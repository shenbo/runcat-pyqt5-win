# https://github.com/yokra9/RunCat_for_Windows_on_PowerShell/blob/master/RunCatPS/src/runcat.ps1
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Win32Functions::ShowWindow
$cscode = @"
    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
"@
$Win32Functions = Add-Type -MemberDefinition $cscode -name Win32ShowWindowAsync -namespace Win32Functions -PassThru
$Win32Functions::ShowWindowAsync((Get-Process -PID $pid).MainWindowHandle, 0) > $null # bool �l��Ԃ��̂� null �Ɏ̂Ă�


$notifyIcon = New-Object System.Windows.Forms.NotifyIcon
$notifyIcon.Visible = $true

# icons
$path = Split-Path -Parent $MyInvocation.MyCommand.Path
$cats = @(
    New-Object System.Drawing.Icon -ArgumentList "$path\\icons\\runcat\\0.ico";
    New-Object System.Drawing.Icon -ArgumentList "$path\\icons\\runcat\\1.ico";
    New-Object System.Drawing.Icon -ArgumentList "$path\\icons\\runcat\\2.ico";
    New-Object System.Drawing.Icon -ArgumentList "$path\\icons\\runcat\\3.ico";
    New-Object System.Drawing.Icon -ArgumentList "$path\\icons\\runcat\\4.ico"
)

# get CPU usage
$job = Start-Job -ScriptBlock {
    Get-Counter -Counter "\Processor(_Total)\% Processor Time" -Continuous | ForEach-Object {
        $_.CounterSamples.CookedValue
    }
}

$cpuTimer = New-Object Windows.Forms.Timer

$script:cpuUsage = 1

$cpuTimer.Add_Tick( {
        $cpuTimer.Stop()
        $script:cpuUsage = [double](Receive-Job $job)[0]
        $cpuTimer.Start()
    })

$cpuTimer.Interval = 3 * 1000
$cpuTimer.Start()

# runner
$animateTimer = New-Object Windows.Forms.Timer

$script:idx = 0

$animateTimer.Add_Tick( {
        $animateTimer.Stop()
  
        $notifyIcon.Icon = $cats[$script:idx++]
        if ($script:idx -eq 5) { $script:idx = 0 }

        $notifyIcon.Text = $script:cpuUsage
        $animateTimer.Interval = (200.0 / [System.Math]::Max(1.0, [System.Math]::Min(20.0, $script:cpuUsage / 5)))

        $animateTimer.Start()
    })
  
$animateTimer.Interval = 200
$animateTimer.Start()

# ApplicationContext
$applicationContext = New-Object System.Windows.Forms.ApplicationContext
  
# click function：quit
$notifyIcon.add_Click( { $applicationContext.ExitThread() })

# run
[System.Windows.Forms.Application]::Run($applicationContext)

# quit
$cpuTimer.Stop()
$animateTimer.Stop()
$notifyIcon.Visible = $false