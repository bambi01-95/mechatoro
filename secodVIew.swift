//
//    func ConvertMessage(){
//        let r = hypotenuse(locx,locy)
//        let alpha = atan2(locy,abs(locx)) / (Double.pi / 2)
//        if(locx > 0){
//            Lvec = r
//            Rvec = -r * alpha
//        }
//        else if(locx < 0){
//            Lvec = -r * alpha
//            Rvec = r
//        }
//        else if(locy > 45){
//            Lvec = 50
//            Rvec = 50
//        }
//        else{
//            Lvec = 0.0
//            Rvec = 0.0
//        }
//        let message = String(Int(Lvec)) + "," + String(Int(Rvec))
//        print(message)
//    }


    @State var Lvec = 0.0
    @State var Rvec = 0.0