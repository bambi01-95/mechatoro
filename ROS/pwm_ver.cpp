// lib for mbed
#include "mbed.h"
// lib for LOS
#include <ros.h>
#include <std_msgs/Float32MultiArray.h>
// lib for other
#include <time.h>

/*
    2023/07/01 bambi01-95 m058　
    not using PID(encoder)
    this only uses pwmout
*/


// wheel motor
PwmOut motL1(D4);  // 
PwmOut motL2(D5);  // 

PwmOut motR1(D11); // 
PwmOut motR2(D10); // 

ros::NodeHandle nh;
std_msgs::Float32MultiArray motor_vels;

float setpointLeft  = 0.0;
float setpointRight = 0.0;

float motorPriod    = 0.2f;//in init motor
 

void set_setpoint_motorLeft(const std_msgs::Float32MultiArray &motor_vel_left){
    setpointLeft = (float)(motor_vel_left.data[0]) / 100;
}
void set_setpoint_motorRight(const std_msgs::Float32MultiArray &motor_vel_right){
    setpointRight = (float)(motor_vel_right.data[0]) / 100;
}

void init_motor(){
    motR1.period(motorPriod); motR2.period(motorPriod); // R morot pirood
    motL1.period(motorPriod); motL2.period(motorPriod); // L motor piriod
    motR1 = 0.0f; motR2 = 0.0f; //L
    motL1 = 0.0f; motL2 = 0.0f; //R
}

void updata_motor_spd(float Lspd,float Rspd){
    if(Lspd>=0){motL1 = abs(Lspd); motL2 = 0.0f;}
    else       {motL1 = 0.0f;      motL2 = abs(Lspd);}

    if(Rspd>=0){motR1 = abs(Rspd); motR2 = 0.0f;}
    else       {motR1 = 0.0f;      motR2 = abs(LspR);}
}


int main()
{
// setting sub
    ros::Subscriber<std_msgs::Float32MultiArray> motor_sub_left("set_setpoint_left_motor",   &set_setpoint_motorLeft);
    ros::Subscriber<std_msgs::Float32MultiArray> motor_sub_right("set_setpoint_right_motor", &set_setpoint_motorRight); //
// setting pub
    ros::Publisher motor_vel_pub("motor_vel", &motor_vels);
    motor_vels.data_length = 2;
    motor_vels.data[0] = 0.0;
    motor_vels.data[1] = 0.0;
// connect ros 
    nh.initNode();
    nh.subscribe(motor_sub_left);
    nh.subscribe(motor_sub_right); 
    nh.advertise(motor_vel_pub);
// init motor
    init_motor();
    while(1) {
        nh.spinOnce();
        updata_motor_spd(set_setpoint_motorLeft,set_setpoint_motorRight);

        motor_vel_pub.publish( &motor_vels );
        wait_ms(10);
    }

}