[cmdletbinding()]
#Declaring parameters for path variable

Param(
[Parameter(Position=0,ValueFromPipeline,ValueFromPipelineByPropertyName)]

[ValidateScript({Test-Path $_})]

[Alias("PSPath")]

[string]$Path = '')
 
Process {
    Write-verbose "Testing hashing with $(Convert-Path $Path)"
    $filesize = (Get-item $path).Length
	#Length of file
 
    $algorithms = "SHA1","SHA256","SHA384","SHA512","MD5" 
    #Recursive for loop
    foreach ($item in $algorithms) {
    [pscustomobject]@{
     Algorithm = $item
     HashTime = Measure-Command { Get-FileHash -Path $Path -Algorithm $item} #Getting Hash value of the file item
     FileSize = $filesize
    }
 
    } #foreach
 
} #process






