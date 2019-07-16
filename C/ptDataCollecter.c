#include "headerFiles.h"

#define PORT 30330
#define BUFFER_SIZE 1024
#define BUFF_SIZE 400
#define LISTEN_QUEUE_SIZE 8

char folder_name[20];
char file_name[20];
//char file_dir[40] = "Data/";
char file_dir[40] = "Data/";

void childHandler(int signal){
    
    int status;
    pid_t spid;

    while((spid = waitpid(-1, &status, WNOHANG))>0){
        printf("PID : %d\n",spid);
        printf("Exit Value : %d\n",WEXITSTATUS(status));
        printf("Exit Stat : %d\n",WIFEXITED(status));
    }
}
void FileCase(char index){
    
    int num = 1;
    DIR *d;
    struct dirent *dir;
    
    switch (index){
	case '1':
	    d = opendir("Data/1/");
	    break;
	case '2':
	    d = opendir("Data/2/");
	    break;
	case '3':
	    d = opendir("Data/3/");
	    break;
	case '4':
	    d = opendir("Data/4/");
	    break;
	case '5':
	    d = opendir("Data/5/");
	    break;
	case '6':
	    d = opendir("Data/6/");
	    break;
	case '7':
	    d = opendir("Data/7/");
	    break;
	case '8':
	    d = opendir("Data/8/");
	    break;
	case '9':
	    d = opendir("Data/9/");
	    break;
	case 'a':
	    d = opendir("Data/a/");
	    break;
    }
    if(d){
        while((dir = readdir(d)) != NULL){
            num++;
	}
	closedir(d);
    }
    sprintf(folder_name,"%c/",index);
    strcat(file_dir,folder_name);

    sprintf(file_name,"%c_%d.csv",index,num-2);
    strcat(file_dir,file_name);
}

int main(){
    signal(SIGCHLD, (void *)childHandler);

    struct sockaddr_in listenSocket;

    memset(&listenSocket, 0, sizeof(listenSocket));
    listenSocket.sin_family = AF_INET;
    listenSocket.sin_addr.s_addr = htonl(INADDR_ANY);
    listenSocket.sin_port = htons(PORT);

    int listenFD = socket(AF_INET, SOCK_STREAM,0);
    int connectFD;

    ssize_t receivedBytes;
    char readBuff[BUFFER_SIZE];
    char sendBuff[BUFFER_SIZE];
    pid_t pid;
    
    struct tm *t;
    time_t rawtime;

    time(&rawtime);
    t = localtime(&rawtime);
    int flag = 0;

    char Index;

    FILE *fp;

    if(bind(listenFD, (struct sockaddr *)&listenSocket, sizeof(listenSocket)) == -1){
        printf("Can not bind.\n");
        return -1;
    }

    if (listen(listenFD, LISTEN_QUEUE_SIZE) == -1){
        printf("Listen fail.\n");
        return -1;
    }

    printf("Waiting for clients...\n");
    
    while(1){
        struct sockaddr_in connectSocket, peerSocket;

        socklen_t connectSocketLength = sizeof(connectSocket);

        while((connectFD = accept(listenFD, (struct sockaddr*)&connectSocket, (socklen_t*)&connectSocketLength))>=0){
            getpeername(connectFD, (struct sockaddr*)&peerSocket, &connectSocketLength);

//            char peerName[sizeof(peerSocket.sin_addr)+1]={0};
            char peerName[sizeof(peerSocket.sin_addr)+10]={0};
            sprintf(peerName, "%s", inet_ntoa(peerSocket.sin_addr));

            if(strcmp(peerName,"0.0.0.0") !=0){
            
                printf("Client : %s\n", peerName);
                printf("%02d%02d%02d connect\n",t->tm_hour,t->tm_min,t->tm_sec);
            }
            else if(connectFD<0){
                printf("Server: accept failed\n");
                exit(0);
            }

            pid = fork();

            if(pid == 0){
                close(listenFD);
                ssize_t receivedBytes;
                
                while((receivedBytes = read(connectFD, readBuff, BUFF_SIZE)) >0){
                    
                    Index = readBuff[0];
                    if(flag == 0){
                        switch (Index) {
                            case '1':
                            FileCase('1');
                            break;
                            case '2':
                            FileCase('2');
                            break;
                            case '3':
                            FileCase('3');
                            break;
                            case '4':
                            FileCase('4');
                            break;
                            case '5':
                            FileCase('5');
                            break;
                            case '6':
                            FileCase('6');
                            break;
                            case '7':
                            FileCase('7');
                            break;
                            case '8':
                            FileCase('8');
                            break;
                            case '9':
                            FileCase('9');
                            break;
                            case 'a':
                            FileCase('a');
                            break;
                        }
                        flag = 1;
                    }
                    printf("\n%lu bytes read\n", receivedBytes);
                    readBuff[receivedBytes]='\0';

                    printf("receive : %s\n", readBuff);
                    
                    printf("%s\n", file_dir);
                    
                    fp = fopen(file_dir, "a");
                    fprintf(fp, "%s", readBuff);

                    if(fp == NULL) printf("file open error");

                    fclose(fp);
                }
                close(connectFD);
                return 0;
            }
            else close(connectFD);
        }
    }
    close(listenFD);
    return 0;
}
