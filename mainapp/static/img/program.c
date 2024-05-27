#include <stdio.h>
#include <stdlib.h>
#define INZECIT(x) (x * 10)
int x = 255;
unsigned char f(int x)
{
    x++;
    return x;
}
void g(int *p)
{
    int v = *(p++);
    *p *= v;
}
int main(int argc, char *argv[])
{
    printf("%s\n", argv[2]);
    printf("%d\n", (int)INZECIT(2.5 + 1.5));
    char *s = "855048106";
    int a = 0;
    while (*s)
    {
        if (*s < 2)
            break;
        ++s;
        a++;
    }
    printf("%d\n", a);
    int b[] = {2, 5, 9};
    g(b);
    printf("%d\n", b[0] + b[1] + b[2]);
    int y = f(x);
    printf("%d\n", x);
    printf("%d\n", y);
    union data
    {
        double d;
        unsigned int t[2];
    } u, *r;
    r = (union data *)malloc(10 * sizeof(union data));
    printf("%s\n", sizeof(r) > 40 ? "alocare" : "dinamica");
    u.d = 20.40;
    u.t[1] += 1 << 20;
    printf("%f\n", u.d);
    free(r);
    return 0;
}