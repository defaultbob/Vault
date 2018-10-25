import ftplib

def main():
    
    ftp = ftplib.FTP()
    ftp.connect('devconfig.vaultdev.com', 22)
    ftp.login("david.mills", "configtoolD3v")

    #ftp.cwd('/usr/local/apache-tomcat/6.0.32/logs')   

    files = []

    try:
        files = ftp.nlst('/data2/devconfigtoolreports')
    except (ftplib.error_perm, resp):
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise

    for f in files[:10]:
        print(f)

if __name__ == '__main__':
    main()
    