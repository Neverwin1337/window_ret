#include <string>

#include <wtypes.h>

std::string Encrypt(std::string content, std::string secretKey)
{
    for (UINT i = 0; i < content.length(); i++)
    {
        content[i] ^= secretKey[i % secretKey.length()];
    }
 
    return content;
}
 
std::string Decrypt(std::string data, std::string secretKey)
{
    for (UINT i = 0; i < data.length(); i++)
    {
        data[i] ^= secretKey[i % secretKey.length()];
    }
 
    return data;
}