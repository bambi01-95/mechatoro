#include "mbed.h"
#include <time.h>
/*-----------------------------------------------*\
                PID test good
\*-----------------------------------------------*/
//phto reflecter
AnalogIn pA(A0); // A Left
AnalogIn pB(A1); // B /A4/
AnalogIn pC(A2); // C /A5/
AnalogIn pD(A3); // D 

// wheel motor
PwmOut motL1(D4);  // R
PwmOut motL2(D5);  // R

PwmOut motR1(D11); // L D11
PwmOut motR2(D10); // L D2

void LRmotor(float d,float b);
float PID1(float b,float d);
void PID2(float input);
#define KP 0.3f
#define KI 10.0f//2.21 //2.2
#define KD 0.001f//1.0 2.0 3.0 0.1//.1 2 3 4 5 6 7 8 9 0//1 2 3 4 5 6 7 8
#define DELTA 0.001

float integral = 0.0f;
float current = 0.0f;
float previous = 0.0f;

int main()
{
    float  b, d,a,c;//, e;   // black rate value
    motR1.period(0.02f); motR2.period(0.02f); // R morot pirood
    motL1.period(0.02f); motL2.period(0.02f); // L motor piriod
    
    motR1 = 0.3f; motR2 = 0.0f; //L
    motL1 = 0.3f; motL2 = 0.0f; //R
        
    while (1)
    {
        clock_t begin = clock();
        b = pB.read();d = pD.read();
        PID2(PID1(b,d));
        clock_t end = clock();
        printf( "result: %f seconds\n", (double)(end - begin) / CLOCKS_PER_SEC );
    }
}


float PID1(float b,float d)
{
    previous = current;
    current =  b - d;
    integral = integral + (current + previous) / 2.0f * DELTA;
    printf("%f\n",integral);
    float PID_1 = (KP * current) + (KI * integral) +  (KD * (current - previous)/DELTA);
    return PID_1;
}

void PID2(float input)
{
    LRmotor(0.30f+input,0.30f-input);
}

void LRmotor(float d,float b){
    motR1 = b;
    motR2 = 0.0f;
    
    motL1 = d;
    motL2 = 0.0f;
}