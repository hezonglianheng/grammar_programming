# Author: Qin Yuhang
# 将pythonPath和scriptPath替换为你的计算机上的相应路径
$pythonPath = "venv\Scripts\python.exe"
$scriptPath = "task2\llm_test\getllm.py"
$gpt4o = "gpt4o"
$claude = "claude"
$ernie = "ernie"
$llama3 = "llama3"
$gemma = "gemma"

$zero = "zero"

# Execute the getllm.py script
& $pythonPath $scriptPath $gpt4o
& $pythonPath $scriptPath $claude
& $pythonPath $scriptPath $ernie
& $pythonPath $scriptPath $llama3
& $pythonPath $scriptPath $gemma
& $pythonPath $scriptPath $gpt4o $zero
& $pythonPath $scriptPath $claude $zero
& $pythonPath $scriptPath $ernie $zero
& $pythonPath $scriptPath $llama3 $zero
& $pythonPath $scriptPath $gemma $zero