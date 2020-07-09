-- Backup database
USE master
DECLARE @vDatabaseName        nvarchar(30)
DECLARE @vBackupNameSuffix    nvarchar(30)    
DECLARE @vBackupFilePath      varchar(500);
DECLARE @vSQL                 nvarchar(2000)
DECLARE @vDeleteFile          nvarchar(1000);

SELECT @vBackupNameSuffix = '_Original.BAK'; -- no postfix

---------------------------------------------------
-- Backup all DBs (except MISC) to F:\MSSQL\Backup
---------------------------------------------------
SELECT @vBackupFilePath   = 'F:\MSSQL\Backup'

-- Backup database Vertex
SELECT @vDatabaseName = 'Vertex'
SELECT @vDeleteFile = @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix
EXECUTE master.dbo.xp_delete_file 0,@vDeleteFile
SELECT @vsql = '
    BACKUP DATABASE ' + @vDatabaseName + ' 
    TO DISK = ''' + @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix + '''
    WITH INIT, STATS;'
EXEC sp_executesql @vsql ;

-- Backup database VertexArch
SELECT @vDatabaseName = 'VertexArch'
SELECT @vDeleteFile = @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix
EXECUTE master.dbo.xp_delete_file 0,@vDeleteFile
SELECT @vsql = '
    BACKUP DATABASE ' + @vDatabaseName + ' 
    TO DISK = ''' + @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix + '''
    WITH INIT, STATS;'
EXEC sp_executesql @vsql ;

-- Backup database Games
SELECT @vDatabaseName = 'Games'
SELECT @vDeleteFile = @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix
EXECUTE master.dbo.xp_delete_file 0,@vDeleteFile
SELECT @vsql = '
    BACKUP DATABASE ' + @vDatabaseName + ' 
    TO DISK = ''' + @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix + '''
    WITH INIT, STATS;'
EXEC sp_executesql @vsql ;

-- Backup database GamesArch
SELECT @vDatabaseName = 'GamesArch'
SELECT @vDeleteFile = @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix
EXECUTE master.dbo.xp_delete_file 0,@vDeleteFile
SELECT @vsql = '
    BACKUP DATABASE ' + @vDatabaseName + ' 
    TO DISK = ''' + @vBackupFilePath + '\' +  @vDatabaseName + @vBackupNameSuffix + '''
    WITH INIT, STATS;'
EXEC sp_executesql @vsql ;
