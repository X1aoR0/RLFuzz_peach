#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main() {
    const char* msg = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    size_t len = strlen(msg);
    size_t total_bytes = 0;


        ssize_t bytes_written = write(STDERR_FILENO, msg, len);
        if (bytes_written == -1) {
            perror("write");
           
        }
        total_bytes += (size_t)bytes_written;
        //fprintf(stderr, "Total bytes written: %lu\n", total_bytes);


    return 0;
}
