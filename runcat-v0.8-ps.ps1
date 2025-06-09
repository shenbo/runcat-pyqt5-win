# 加载 .NET 程序集
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

# 创建托盘图标对象
$notifyIcon = New-Object System.Windows.Forms.NotifyIcon
$notifyIcon.Text = "PowerShell Notify Icon"
$notifyIcon.Visible = $true

# 加载图标, base64
$base64Icons = @(
    "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"
)

$loadedIcons = $base64Icons | ForEach-Object {
    $iconBytes = [Convert]::FromBase64String($_)
    $memoryStream = New-Object System.IO.MemoryStream($iconBytes, 0, $iconBytes.Length)
    $memoryStream.Write($iconBytes, 0, $iconBytes.Length)
    $bitmap = [System.Drawing.Bitmap]::FromStream($memoryStream)
    $icon = [System.Drawing.Icon]::FromHandle($bitmap.GetHicon())
    $memoryStream.Dispose()
    $bitmap.Dispose()
    $icon
}
Write-Host "load ", $loadedIcons.Count, " icons"

# 设置初始图标
$notifyIcon.Icon = $loadedIcons[0]

# 获取 CPU 使用率
$script:cpuUsage = 0.1
$job = Start-Job -ScriptBlock {
    Get-Counter -Counter "\Processor(_Total)\% Processor Time" -Continuous | ForEach-Object { $_.CounterSamples.CookedValue }
}
# 线程1 
$cpuTimer = New-Object System.Windows.Forms.Timer
$cpuTimer.Interval = 1000
$cpuTimer.Add_Tick({
        $cpuTimer.Stop()
        $script:cpuUsage = (Receive-Job $job)
        $cpuTimer.Start()
    })
$cpuTimer.Start()

# 线程2 切换图标
$script:iconIndex = 0
$timer = New-Object System.Windows.Forms.Timer
$timer.Add_Tick({
        $notifyIcon.Icon = $loadedIcons[($script:iconIndex ++) % $loadedIcons.Count]
        $notifyIcon.Text = ("Cpu Usage: {0:f2}%: " -f $script:cpuUsage)
        $timer.Interval = 200 - $script:cpuUsage * 1.5
        Write-Host ("Cpu Usage: {0:f2}%;  Icon Update Interval: {1:d3}ms" -f $script:cpuUsage, $timer.Interval)
    })
$timer.Start()

# 添加右键菜单: quit
$contextMenu = New-Object System.Windows.Forms.ContextMenuStrip
$exitMenuItem = New-Object System.Windows.Forms.ToolStripMenuItem
$exitMenuItem.Text = "quit"
$exitMenuItem.Add_Click({
        $timer.Stop()
        $cpuTimer.Stop()
        Stop-Job $job
        Remove-Job $job
        $loadedIcons | ForEach-Object { $_.Dispose() }
        $notifyIcon.Visible = $false
        [System.Windows.Forms.Application]::Exit()
    })
$contextMenu.Items.Add($exitMenuItem)
$notifyIcon.ContextMenuStrip = $contextMenu

# 保持脚本运行
[System.Windows.Forms.Application]::Run()
