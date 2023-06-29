#include <iostream>
#include <winsock2.h>
#include <windows.h>
#include <string>
#include <vector>
#include <stdio.h>


#pragma warning(disable:4996)
#pragma comment(lib, "ws2_32.lib")

SOCKET clientSocket;
SOCKET MclientSocket;
HANDLE hMouseThread;

int SendImageData(SOCKET serverSocket);

void split(char* src, const char* separator, char** dest) {
    char* pNext;
    int count = 0;
    if (src == NULL || strlen(src) == 0)
        return;
    if (separator == NULL || strlen(separator) == 0)
        return;
    pNext = strtok(src, separator);
    while (pNext != NULL) {
        *dest++ = pNext;
        ++count;
        pNext = strtok(NULL, separator);
    }
}

DWORD WINAPI mouse(LPVOID lpThreadParameter) {
    MclientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (MclientSocket == INVALID_SOCKET)
    {
        std::cerr << "Failed to create socket." << std::endl;
        WSACleanup();
        return 1;
    }
    sockaddr_in serverAddress{};
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(12345);
    serverAddress.sin_addr.s_addr = inet_addr("192.168.50.10");
    if (connect(MclientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0)
    {
        std::cerr << "Connection failed." << std::endl;
        closesocket(MclientSocket);
        WSACleanup();
        return 1;
    }

    std::cout << "Connected to server." << std::endl;
    int ret;
    send(MclientSocket, "MOUSE_T", sizeof("MOUSE_T"), 0);
    while (1) {
        char buf[1000];
        char* attack[100] = { 0 };
        ret = recv(MclientSocket, buf, sizeof(buf), 0);

        if (ret < 0) {
            return 1;
        }
        if (ret > 0) {
            buf[ret] = 0x00;
            std::cout << buf << std::endl;
            split(buf, " ", attack);

            if (strncmp(attack[0], "LD", 2) == 0) {
                SetCursorPos(atoi(attack[1]), atoi(attack[2]));
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);

            }
            else if (strncmp(attack[0], "RD", 2) == 0) {
                SetCursorPos(atoi(attack[1]), atoi(attack[2]));
                mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0);

            }
            else if (strncmp(attack[0], "LU", 2) == 0) {
                SetCursorPos(atoi(attack[1]), atoi(attack[2]));
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);

            }
            else if (strncmp(attack[0], "RU", 2) == 0) {
                SetCursorPos(atoi(attack[1]), atoi(attack[2]));
                mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0);

            }
            else if (strncmp(attack[0], "MM", 2) == 0) {
                SetCursorPos(atoi(attack[1]), atoi(attack[2]));
                mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0);
            }

        }
    }
}

int screen() {
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == INVALID_SOCKET)
    {
        std::cerr << "Failed to create socket." << std::endl;
        WSACleanup();
        return 1;
    }
    sockaddr_in serverAddress{};
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(12345);
    serverAddress.sin_addr.s_addr = inet_addr("192.168.50.10");
    if (connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0)
    {
        std::cerr << "Connection failed." << std::endl;
        closesocket(clientSocket);
        WSACleanup();
        return 1;
    }

    std::cout << "Connected to server." << std::endl;

    send(clientSocket, "SCREEN_T", sizeof("SCREEN_T"), 0);

    char tmp_l[10];
    char tmp_2[10];
    snprintf(tmp_l, 10, "%d", GetSystemMetrics(SM_CXSCREEN));
    snprintf(tmp_2, 10, "%d", GetSystemMetrics(SM_CYSCREEN));
    int ret;
    char buf1[10];
    ret = recv(clientSocket, buf1, sizeof(buf1), 0);
    buf1[ret] = 0x00;
    if (strncmp(buf1, "cx", 2) == 0) {
        send(clientSocket, tmp_l, strlen(tmp_l), 0);
    }
    memset(buf1, 0x00, sizeof(buf1));
    ret = recv(clientSocket, buf1, sizeof(buf1), 0);
    buf1[ret] = 0x00;
    if (strncmp(buf1, "cy", 2) == 0) {
        send(clientSocket, tmp_2, strlen(tmp_l), 0);
    }

    while (true) {
        int ec = SendImageData(clientSocket);
        if (ec == 1) {
            break;
        }
    }

    // Close the mouse thread
    if (hMouseThread != NULL) {
        TerminateThread(hMouseThread, 0);
        CloseHandle(hMouseThread);
    }

    return 1;
}

int SendImageData(SOCKET serverSocket) {
    CURSORINFO pci;
    pci.cbSize = sizeof(CURSORINFO);
    GetCursorInfo(&pci);
    POINT point = pci.ptScreenPos;

    ICONINFO iconinfo;
    GetIconInfo(pci.hCursor, &iconinfo);
    const char sourceString[8] = "DISPLAY";
    int bufferSize = MultiByteToWideChar(CP_UTF8, 0, sourceString, -1, NULL, 0);
    wchar_t* targetString = new wchar_t[bufferSize];
    MultiByteToWideChar(CP_UTF8, 0, sourceString, -1, targetString, bufferSize);

    // 使用转换后的宽字符字符串（targetString）进行操作，如传递给接受 LPCWSTR 类型的函数等

    
    HDC hdc = CreateDC(targetString, NULL, NULL, NULL);
    
    HDC memdc = CreateCompatibleDC(hdc);
    HDC memdc1 = CreateCompatibleDC(hdc);
    HDC memdc2 = CreateCompatibleDC(hdc);
    SelectObject(memdc, iconinfo.hbmMask);
    SelectObject(memdc1, iconinfo.hbmColor);

    int srcxsize = GetSystemMetrics(SM_CXSCREEN);
    int srcysize = GetSystemMetrics(SM_CYSCREEN);
    HBITMAP hBitmap = CreateCompatibleBitmap(hdc, srcxsize, srcysize);
    SelectObject(memdc2, hBitmap);
    BitBlt(memdc2, 0, 0, srcxsize, srcysize, hdc, 0, 0, SRCCOPY);
    BitBlt(memdc2, point.x, point.y, 20, 20, memdc, 0, 0, SRCAND);
    BitBlt(memdc2, point.x, point.y, 20, 20, memdc1, 0, 0, SRCPAINT);

    BITMAP bitmap;
    GetObject(hBitmap, sizeof(BITMAP), &bitmap);

    int imageSize = bitmap.bmWidthBytes * bitmap.bmHeight;

    std::vector<char> buffer(imageSize);
    GetBitmapBits(hBitmap, imageSize, buffer.data());

    if (send(serverSocket, (char*)&imageSize, sizeof(int), 0) == SOCKET_ERROR)
    {
        std::cerr << "Failed to send image size." << std::endl;
        delete[] targetString;
        return 1;
    }

    int bytesSent = 0;
    while (bytesSent < imageSize)
    {
        int result = send(serverSocket, buffer.data() + bytesSent, imageSize - bytesSent, 0);
        if (result == SOCKET_ERROR)
        {
            std::cerr << "Failed to send image data." << std::endl;
            delete[] targetString;
            return 1;
        }
        bytesSent += result;
    }

    DeleteObject(hBitmap);
    ReleaseDC(NULL, hdc);
    delete[] targetString;
    return 0;
}

DWORD WINAPI look_init(LPVOID lpParamter)
{
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        std::cerr << "Failed to initialize WinSock." << std::endl;
        return 1;
    }

    //hMouseThread = CreateThread(NULL, 0, mouse, NULL, 0, NULL);
    screen();

    closesocket(clientSocket);
    closesocket(MclientSocket);
    WSACleanup();

    return 0;
}
