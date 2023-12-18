#/usr/bin/env python3

from os import system , path , chdir , environ
import json

__version__ = "0.2.1"


""" in SettingFile class"""
class SettingFile:
    def __init__( self ):
        self.SettingFile = "/etc/rhenium/SettingFile.json"
        self.settings = {}
        self.os_ids = {
            "1":"arch",
            "2":"fedora",
            "3":"opensuse",
            "4":"cent os",
            "5":"alpine",
            "6":"gentoo",
            "7":"freebsd",
            "8":"netbsd",
            "9":"openbsd",
            "10":"debian",
            "11":"ubuntu",
            "12":"void",
            "13":"dragonfly"
        }
        
        if not path.exists( "/etc/rhenium/SettingFile.json" ):
            self.setup()
        else:
            self.load()
            if self.settings.get("version") != __version__:
                print( "[*] setting up Rhenium Installer after updates..." )
                self.setup()

    def load( self ):
        file_descriptor = open( self.SettingFile , "r" )
        self.settings = json.loads(file_descriptor.read())
        file_descriptor.close()

    def save( self ):
        try:
            file_descriptor = open( self.SettingFile , "w" )
        except PermissionError:
            print( "[!] you must be root to do any changes to the settings" )
            exit(-1)
        file_descriptor.write( json.dumps( self.settings ) )
        file_descriptor.close()


    def setup( self ):
        print( "current settings:\n" )
        if self.settings != {}:
            print( "\tos :" , self.settings["os"] )
            choice = input( "\nDo you want to change the current options? [Y/N]  " )
            if choice.strip().lower() != "y":
                exit(0)
        else:
            print("[*] setting Rhenium automated setup for the first time...\n\n")
        
        print( "What is the Linux disribution that you are using?" )
        print( "\t1)   Arch Linux" )
        print( "\t2)   Fedora Linux" )
        print( "\t3)   OpenSUSE Linux" )
        print( "\t4)   CentOS" )
        print( "\t5)   Apline Linux" )
        print( "\t6)   Gentoo Linux" )
        print( "\t7)   FreeBSD" )
        print( "\t8)   NetBSD" )
        print( "\t9)   OpenBSD" )
        print( "\t10)  Debian Linux" )
        print( "\t11)  Ubuntu Linux" )
        print( "\t12)  Void Linux" )
        print( "\t13)  DragonFly BSD" )
        
        print( "\n\ttype 0 to exit" )

        choice = str(input( "your choice: " ))

        if choice.strip() in list(self.os_ids.keys()):
            self.settings["os"] = self.os_ids[choice.strip()]
            self.settings["version"] = __version__
            self.save()
        else:
            print( "you have to choose on of the given numbers only" )


class InstallFile:
    def __init__( self ):
        file_descriptor = open( "/etc/rhenium/HardwareInfo" , "r" )
        self.info = file_descriptor.read()
        file_descriptor.close()
        settingObj = SettingFile()
        self.settings = settingObj.settings
        del settingObj
        self.selectors = ["pci" , "path" , "os"]


    def _check_pci( self, device ):
        return  device in self.info

    def _check_path( self , fsys_path ):
        return  path.exists( fsys_path )

    def _check_os( self , os ):
        os = os.strip()
        return self.settings.get("os") == os
    
    def cd( self , dir_path ):
        try:
            chdir( path.expanduser(path.strip()) )
        except Exception as error:
            print( "cd: " , error )
            exit(-1)
    
    def export_env( self , statement ):
        if not ("=" in statement):
            print( "Export ERROR:   expected '=' to separate the variable and the value." )
            return False
        
        var = statement[ :statement.index("=") ].lstrip()
        val = statement[ statement.index("=")+1 : ].rstrip()

        if var[0] == "\"" or var[0] == "\'" or var[0] == "`":
            var = var[1:]
        if var[-1] == "\"" or var[-1] == "\'" or var[-1] == "`":
            var = var[:-1]

        if val[-1] == ";":
            val = val[:-1]
        if val[0] == "\"" or val[0] == "\'" or val[0] == "`":
            val = val[1:]
        if val[-1] == "\"" or val[-1] == "\'" or val[-1] == "`":
            val = val[:-1]

        while "$" in val and val[val.index("$")-1] != "\\":
            pos = val.index("$")
            while( val[pos-1] == "\\" ):
                pos = val[pos+1:].index("$")
            
            env_var = ""
            i = pos+1
            while i<len(val) and ( val[i].isalnum() or val[i] == "_" ):
                env_var += val[i]
                i+=1

            if environ.get( env_var ) == None:
                print( "Export ERROR:   the environment variable" , env_var , "do not exist" )
                return False

            val = val.replace( "$"+env_var , environ[env_var] )
            
    
        
        environ[ var ] = val
        return True

    def parse( self , scriptline ):

        index = 0
        
        selector = ""
        params = ""
        should_execute = True

        parsed = []

        if scriptline.strip() == "exec":
            return [{
                "selector": "exec",
                "should-exist":None,
                "params":None
            }]

        elif ("{" in scriptline):
            index = scriptline.index("{")
            selector = scriptline[ :index ].strip()
            if "not" in selector:
                should_execute = False
                selector = selector[:-3].strip()
            
            if not( selector in self.selectors):
                return "\"" + selector + "\" is not a valid option. this can be only one of the followings: \"exec\" , \"pci\" , \"path\" or \"os\"."
            
            if "}" in scriptline[index:]:
                params = scriptline[ index+1:scriptline.index("}") ]

                parsed.append({
                    "selector":selector ,
                    "should-exist":should_execute ,
                    "params":params
                })

                next_token = scriptline[ scriptline.index("}")+1: ].strip()
                if next_token != "":
                    if next_token[:4] == "and " or next_token[:4] == "and\t":
                        parsed.append("and")
                        next_token = next_token[4:]


                    elif next_token[:3] == "or " or next_token[:3] == "or\t":
                        parsed.append("or")
                        next_token = next_token[3:]

                    else:
                        if " " in  next_token:
                            return "unexpected token \""+next_token[:next_token.find(" ")].strip()+"\" after \"}\" you should use \"or\" or \"and\" or you can leave it empty"
                        else:
                            return "unexpected token \""+next_token.strip()+"\" after \"}\" you should use \"or\" or \"and\" or you can leave it empty"
                    p = self.parse( next_token )
                    if type(p) != str:
                        for element in p:
                            parsed.append( element )
                        return parsed
                    else:
                        return p
                
                return parsed
            else:
                return "you should not leave {...} open"
            
        else:
            return "you need to add your parameters inside {...}"

    def should_exec( self , parser_params ):
        last_condition = self._check_exec( parser_params[0] )
        
        i = 1
        while i < len( parser_params ):
            if parser_params[ i ] == "and":
                i += 1
                last_condition = last_condition and self._check_exec( parser_params[ i ] )
            elif parser_params[ i ] == "or":
                i += 1
                last_condition = last_condition or self._check_exec( parser_params[ i ] )
            else:
                print( "ERROR No.2: please report this error you should not see this if Rhenium Installer is running as intended" )
                exit(-1)
            i += 1
        
        return last_condition


    def _check_exec( self ,  parse_param ):
        # PCI
        if parse_param["selector"] == "pci":
            if parse_param["should-exist"]:
                return self._check_pci( parse_param["params"] )
            else:
                return not self._check_pci( parse_param["params"] )
        
        # Path
        elif parse_param["selector"] == "path":
            if parse_param["should-exist"]: 
                return self._check_path( parse_param["params"] )
            else:
                return not self._check_path( parse_param["params"] )
        
        # OS
        elif parse_param["selector"] == "os":
            if parse_param["should-exist"]: 
                return self._check_os( parse_param["params"] )
            else:
                return not self._check_os( parse_param["params"] )

        # Execute
        elif parse_param["selector"] == "exec":
            return True

        else:
            print( "ERROR No.1: please report this error you should not see this if Rhenium is running as intended" )
            exit(-1)

    def execute( self, filename , debug=False ):
        file_stream = open( filename , "r" )

        script = ""
        keep_going = False
        should_execute = True
        counter = 0
        
        for line in file_stream:
            counter += 1
            
            if line.strip() == "":
                continue
            
            elif line.strip()[0] == "#":
                continue

            elif line.strip()[:2] == "cd":
                self.cd( line.strip()[2:] )
                continue
            elif line.strip()[:6] == "export":
                if debug:
                    print(  counter , " |\texecuting export:" , line[:-1] )
                self.export_env( line.strip()[7:] )
            
            elif keep_going:
                if line.strip() == "end":
                    if debug:
                        if should_execute:
                            print( "\033[32m" , counter , "|  end \033[0m\n" )
                    keep_going = False

                elif should_execute:
                    if debug:
                        print(  counter , " |\texecuting:" , line[:-1] )
                    system( line )
            else:
                p = self.parse( line )
                if type(p) == str:
                    print("\n\n \033[31mSYNTAX ERROR: the InstallFile is written incorrectly \033[0m")
                    print( "\033[33m [!] " , counter , "|\033[0m\t" , line[:-1] )
                    print( "\033[31m in line" , counter , "\033[0m: \033[33m" , p , "\033[0m" )
                    exit(-1)
                else:
                    should_execute = self.should_exec( p )
                    keep_going = True
                    if debug:
                        if p[0]["selector"] == "exec":
                            print( "\033[32m", counter , " |   exec \033[0m    \033[33mexecuting shell script\033[0m" ) 
                        elif should_execute:
                                print( "\033[32m", counter , " | " , line[:-1] , "     [condition was met]\033[0m" )
                        else:
                            print( "\033[90m", counter , " | " , line[:-1] , "      [condition was not met]\033[0m" )
        file_stream.close()
