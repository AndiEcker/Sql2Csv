'''
Created on Jun 22, 2010

@author: andi
'''
import sys
import ConfigParser
#import ceODBC as dbapi
try:
    import pyodbc as dbapi
except ImportError:
    try:
        import ceODBC as dbapi
    except ImportError:
        import sqlite3 as dbapi
    
from lxml import etree

MoConfig = None

def main():
    global MoConfig
    print("Sql2Csv - ODBC database djump tool V2.1 -  (c)2010 Andreas Ecker")
    try:
        # check parameter, set default values
        lArgs = sys.argv
        sOutFileName = None
        sXmlFileName = None
        if len(lArgs) == 1:
            sIniFileName = "Sql2Csv.ini"
        else:
            sIniFileName = lArgs[1]
            if len(lArgs) >= 3:
                sOutFileName = lArgs[2]
                if len(lArgs) >= 4:
                    sXmlFileName = lArgs[3]
                
        # prepare ini file parser
        MoConfig = ConfigParser.RawConfigParser()
        fp = open(sIniFileName, 'r')    # 'w' needed for add_section/set/...
        MoConfig.readfp(fp)
        fp.close()
        # out file settings    
        if sOutFileName == None:
            sOutFileName = IniFileString("Command", "OutFileName", "sql2csv.csv")
        sOutColHeader = IniFileString("Command", "OutFileColumnHeader", "")
        sOutFileColSep = IniFileString("Command", "OutFileColumnSeperator", ";")
        sOutFileLineSep =IniFileString( "Command", "OutFileLineSeperator", "\r\n")
        # xml join settings
        if sXmlFileName == None:    # used as flag to enable xml merge/join
            sXmlFileName = IniFileString("Command", "XmlFileName", None)
        nSqlOverwriteColI = IniFileInt("Command", "SqlOverwriteColumnIndex", "1")
        nSqlJoinColI = IniFileInt("Command", "SqlJoinColumnIndex", "2")
        nXmlJoinColI = IniFileInt("Command", "XmlJoinColumnIndex", "0")
        nXmlSelColI = IniFileInt("Command", "XmlSelectColumnIndex", "5")
        nXmlColCntMax = IniFileInt("Command", "XmlColumnCountMaximum", "6")
        sXmlRowTagName = IniFileString("Command", "XmlRowTagName", '{#RowsetSchema}row')
        bSplitXmlJoinCol = IniFileInt("Command", "SplitXmlJoinColumn", "1")
        bHideXmlSelColZeroes = IniFileInt("Command", "HideXmlSelectColumnZeroes", "0")
        bCnvDecCommaXmlSelColVal = IniFileInt("Command", "ConvertDecimalCommaInXmlSelectColumnValue", "0")
        # database settings
        sConnect = IniFileString("Command", "Connect", "")
        sSqlQuery = IniFileString("Command", "SqlQuery", "")
        bAutoCommit = IniFileInt("Command", "AutoCommit", "0")
        if sConnect == "" or sSqlQuery == "":
            print("Error: Missing Connect/SqlQuery strings in INI file: " + sIniFileName)
            sys.exit(1) 
    except Exception, ex:
        print("startup error: ", ex)
        sys.exit(1) 

    print("...Processing settings in configuration file " + sIniFileName)
    try:
        if sXmlFileName:        # read and pre-process XML file (both optional)
            print("...Loading XML file data from " + sXmlFileName)
            lXmlCols = Xml2ColRowArray(sXmlFileName, nXmlColCntMax, sXmlRowTagName)
            if bSplitXmlJoinCol:
                for nRowI in range(len(lXmlCols[nXmlJoinColI])):
                    lXmlCols[nXmlJoinColI][nRowI] = lXmlCols[nXmlJoinColI][nRowI].split()[0]
        # prepare out file buffer
        sOutLines = []
        if sOutColHeader:
            sOutLines.append(sOutColHeader + sOutFileLineSep)
        print("...Loading query data from " + sConnect)      # open and fetch from database
        cn = dbapi.connect(sConnect, autocommit=bAutoCommit)
        oCursor = cn.cursor()
        oCursor.execute(sSqlQuery)
        for lColVals in oCursor:
            sLine = ''
            for nColI in range(len(oCursor.description)):
                # each column descr: (name, type, display_size, internal_size, precision, scale, null_ok)
                sLine += sOutFileColSep
                sColVal = None
                if nColI == nSqlOverwriteColI:
                    try:
                        nXmlRowI = lXmlCols[nXmlJoinColI].index(lColVals[nSqlJoinColI])
                    except ValueError:
                        nXmlRowI = -1
                    if nXmlRowI >= 0:
                        sColVal = lXmlCols[nXmlSelColI][nXmlRowI]
                        if bCnvDecCommaXmlSelColVal:
                            sColVal = sColVal.replace(',', '.')
                if sColVal == None or (bHideXmlSelColZeroes and toFloat(sColVal) == 0):
                    sColVal = str(lColVals[nColI])
                sLine += sColVal
            sLine += sOutFileLineSep
            sOutLines.append(sLine[len(sOutFileColSep):])
        print("...writing data into " + sOutFileName)    # write line buffer to out file
        outfp = open(sOutFileName, 'w')
        outfp.writelines(sOutLines)
        outfp.close()
        print("Finished without errors.")
        sys.exit(0)
    except dbapi.DataError, ex:
        print("data error: ", ex)
        sys.exit(3) 
    except dbapi.DatabaseError, ex:
        print("database error: ", ex)
        sys.exit(2) 
    except Exception, ex:
        print("fetch/write error: ", ex)
        sys.exit(4) 


def IniFileString(section, option, default):
    if MoConfig.has_option(section, option):
        sRet = MoConfig.get(section, option)
    else:
        sRet = default
    return sRet

def IniFileInt(section, option, default):
    return toInt(IniFileString(section, option, default))

def Xml2ColRowArray(sXmlFilename, nXmlColCntMax, sXmlRowTagName):
    lTree = etree.iterparse(sXmlFilename, tag = sXmlRowTagName)
    lRet = [[] for _ in range(nXmlColCntMax)]
    for _, oElement in lTree:
        nColI = 0
        for sKey in oElement.keys():  # use .getchildren to process sub-elements
            if nColI >= nXmlColCntMax:
                break
            lRet[nColI].append(oElement.get(sKey))
            nColI += 1     
    return lRet  
        
def toInt(sVal):
    try:
        return int(sVal)
    except:
        return 0
    
def toFloat(sVal):
    try:
        return float(sVal)
    except:
        return 0.0
    

if __name__ == '__main__':
    main()
