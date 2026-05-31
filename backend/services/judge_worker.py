import asyncio
import base64
import os
import subprocess
import tempfile
import requests
from pathlib import Path
from sqlmodel import select

from database import async_session_maker, PROJECT_ROOT
from models import Submission, Problem, TestCase, SubmissionResult

# 内存中的异步评测队列
judge_queue = asyncio.Queue()

JUDGE0_API_URL = os.environ.get("JUDGE0_API_URL", "https://judge0-ce.p.rapidapi.com")
JUDGE0_API_KEY = os.environ.get("JUDGE0_API_KEY", "")

JUDGE0_LANG_MAP = {
    "cpp": 54, "c++": 54, "c++17": 54,
    "c": 50,
    "python": 71, "py": 71, "python3": 71,
    "java": 62,
    "js": 63, "javascript": 63,
    "go": 60,
    "rust": 73,
}

def judge0_submit_sync(code: str, language: str, stdin_text: str, timeout_s: float):
    if JUDGE0_API_URL == "local":
        if language.lower() in ["python", "py", "python3"]:
            try:
                res = subprocess.run(["python3", "-c", code], input=stdin_text, text=True, capture_output=True, timeout=timeout_s)
                if res.returncode == 0:
                    return {"status": "OK", "stdout": res.stdout, "message": "", "time_ms": 10}
                else:
                    return {"status": "RE", "stdout": res.stdout, "message": res.stderr, "time_ms": 10}
            except subprocess.TimeoutExpired:
                return {"status": "TLE", "stdout": "", "message": "运行超时", "time_ms": int(timeout_s * 1000)}
            except Exception as e:
                return {"status": "SE", "stdout": "", "message": str(e), "time_ms": 0}
        elif language.lower() in ["cpp", "c++", "c"]:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = Path(tmpdir) / "main.cpp"
                exe = Path(tmpdir) / "a.out"
                src.write_text(code, encoding="utf-8")
                cpp_compiler = os.environ.get("CPP_COMPILER", "g++")
                comp = subprocess.run([cpp_compiler, "-O2", "-std=c++17", str(src), "-o", str(exe)], capture_output=True, text=True)
                if comp.returncode != 0:
                    return {"status": "CE", "stdout": "", "message": comp.stderr, "time_ms": 0}
                try:
                    res = subprocess.run([str(exe)], input=stdin_text, text=True, capture_output=True, timeout=timeout_s)
                    if res.returncode == 0:
                        return {"status": "OK", "stdout": res.stdout, "message": "", "time_ms": 10}
                    else:
                        return {"status": "RE", "stdout": res.stdout, "message": res.stderr, "time_ms": 10}
                except subprocess.TimeoutExpired:
                    return {"status": "TLE", "stdout": "", "message": "运行超时", "time_ms": int(timeout_s * 1000)}
                except Exception as e:
                    return {"status": "SE", "stdout": "", "message": str(e), "time_ms": 0}
        else:
            return {"status": "CE", "stdout": "", "message": f"本地原生模式暂不支持该语言: {language}", "time_ms": 0}

    lang_id = JUDGE0_LANG_MAP.get(language.lower())
    if not lang_id:
        return {"status": "CE", "stdout": "", "message": f"Judge0 暂不支持语言: {language}", "time_ms": 0}

    payload = {
        "source_code": base64.b64encode(code.encode("utf-8")).decode("utf-8"),
        "language_id": lang_id,
        "stdin": base64.b64encode(stdin_text.encode("utf-8")).decode("utf-8"),
        "cpu_time_limit": timeout_s
    }

    headers = {"Content-Type": "application/json"}
    if "rapidapi" in JUDGE0_API_URL:
        host = JUDGE0_API_URL.replace("https://", "").replace("http://", "").split("/")[0]
        headers["x-rapidapi-host"] = host
        if JUDGE0_API_KEY:
            headers["x-rapidapi-key"] = JUDGE0_API_KEY

    try:
        url = f"{JUDGE0_API_URL}/submissions?base64_encoded=true&wait=true"
        resp = requests.post(url, json=payload, headers=headers, timeout=max(timeout_s + 5, 10))
        resp.raise_for_status()
        data = resp.json()

        status_id = data.get("status", {}).get("id", 0)
        time_elapsed = int(float(data.get("time") or 0) * 1000)

        stdout_raw = data.get("stdout")
        stdout = base64.b64decode(stdout_raw).decode("utf-8") if stdout_raw else ""

        compile_output_raw = data.get("compile_output")
        compile_output = base64.b64decode(compile_output_raw).decode("utf-8", errors="replace") if compile_output_raw else ""

        message_raw = data.get("message")
        stderr = base64.b64decode(message_raw).decode("utf-8", errors="replace") if message_raw else ""

        err_msg = compile_output or stderr

        if status_id == 3 or status_id == 4:
            return {"status": "OK", "stdout": stdout, "message": "", "time_ms": time_elapsed}
        elif status_id == 5:
            return {"status": "TLE", "stdout": stdout, "message": "运行超时", "time_ms": time_elapsed}
        elif status_id == 6:
            return {"status": "CE", "stdout": "", "message": err_msg, "time_ms": 0}
        elif 7 <= status_id <= 12:
            return {"status": "RE", "stdout": stdout, "message": err_msg, "time_ms": time_elapsed}
        else:
            return {"status": "SE", "stdout": stdout, "message": f"Judge0 System Error: {status_id} {err_msg}", "time_ms": 0}

    except requests.RequestException as exc:
        return {"status": "SE", "stdout": "", "message": f"API调用失败: {str(exc)}", "time_ms": 0}


async def process_submission(submission_id: int):
    print(f"[评测机] 开始处理提交记录 #{submission_id}...")
    
    async with async_session_maker() as db:
        result = await db.exec(select(Submission).where(Submission.id == submission_id))
        submission = result.first()
        if not submission:
            return

        result = await db.exec(select(Problem).where(Problem.id == submission.problem_id))
        problem = result.first()
        
        result = await db.exec(select(TestCase).where(TestCase.problem_id == submission.problem_id).order_by(TestCase.sort_order))
        cases = result.all()
        
        if not problem or not cases:
            submission.status = "SE"
            await db.commit()
            return

        # 清空旧结果
        await db.exec(select(SubmissionResult).where(SubmissionResult.submission_id == submission_id))
        # 实际开发中可以通过 delete()，为了简便暂不处理多余记录
        
        final_status = "AC"
        timeout_s = max(0.1, problem.time_limit_ms / 1000)
        max_time_ms = 0
        max_memory_kb = 0

        for case in cases:
            input_path = PROJECT_ROOT / case.input_path
            output_path = PROJECT_ROOT / case.output_path
            try:
                stdin_text = input_path.read_text(encoding="utf-8")
                expected_output = output_path.read_text(encoding="utf-8")
            except OSError as exc:
                final_status = "SE"
                db.add(SubmissionResult(submission_id=submission_id, testcase_id=case.id, status="SE", message=str(exc)))
                break

            # 使用 to_thread 防止阻塞事件循环
            run_result = await asyncio.to_thread(
                judge0_submit_sync,
                submission.code, submission.language, stdin_text, timeout_s
            )
            
            status = run_result["status"]
            if status == "OK":
                status = "AC" if run_result["stdout"].rstrip() == expected_output.rstrip() else "WA"

            current_time = run_result.get("time_ms", 0)
            current_memory = run_result.get("memory_kb", 0)
            max_time_ms = max(max_time_ms, current_time)
            max_memory_kb = max(max_memory_kb, current_memory)

            db.add(
                SubmissionResult(
                    submission_id=submission_id,
                    testcase_id=case.id,
                    status=status,
                    time_ms=current_time,
                    memory_kb=current_memory,
                    message=run_result.get("message") or "",
                )
            )

            if status != "AC":
                final_status = status
                break

        submission.status = final_status
        submission.time_ms = max_time_ms
        submission.memory_kb = max_memory_kb
        await db.commit()
        print(f"[评测机] 提交记录 #{submission_id} 状态已更新为: {final_status}, 用时: {max_time_ms}ms, 内存: {max_memory_kb}KB")

async def judge_worker_loop():
    print("[评测机] 后台队列循环已启动，等待评测任务...")
    while True:
        try:
            submission_id = await judge_queue.get()
            await process_submission(submission_id)
            judge_queue.task_done()
        except Exception as e:
            print(f"[评测机] 处理失败: {e}")
