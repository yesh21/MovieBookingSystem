$current_location = Get-Location

$project_folder = $PSScriptRoot + "\.."
Set-Location -Path $project_folder
$scripts_folder = $project_folder + "\venv\Scripts"

. "$($scripts_folder)\python.exe" --version
. "$($scripts_folder)\flake8.exe"
. "$($scripts_folder)\pytest.exe"

Set-Location -Path $current_location