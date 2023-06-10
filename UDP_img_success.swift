//
//  streamView.swift
//  mecha_test
//
//  Created by Hiroto SHIKADA on 2023/06/08.
//
/*  6月10日(土) 動画のやつ　*/
/* observar Frame でできるか*/
import SwiftUI
import Foundation
import Network



struct streamView: View {
    @ObservedObject var Stream = streamFrames()
    
    var body: some View {
        VStack{
            Text("this is img from PC/RasPi")
            if let uiImage = UIImage(data: Stream.img_data) {
                Image(uiImage: uiImage)
                    .frame(width: 300, height: 300)
                    .border(.black, width: 2)
                    .padding()
            }
        }.onAppear{
            Stream.self.myOnButton(0)
        }
        .onDisappear{
            Stream.self.myOffButton(0)
        }
    }
    
}



class streamFrames : ObservableObject {
    @Published var img_data: Data = Data()
    var img_stock = Data()
    
    
    var udpListener:NWListener?
    var backgroundQueueUdpListener   = DispatchQueue(label: "udp-lis.bg.queue", attributes: [])
    var backgroundQueueUdpConnection = DispatchQueue(label: "udp-con.bg.queue", attributes: [])
            
    var connections = [NWConnection]()
    func viewDidLoad() {
        myOnButton(self)
    }
    
    
    func myOnButton(_ sender: Any) {
        
        guard self.udpListener == nil else {
            print(" 🧨 Already listening. Not starting again")
            return
        }
        
        do {
            self.udpListener = try NWListener(using: .udp, on: 8080)// port
            self.udpListener?.stateUpdateHandler = { (listenerState) in
                
                switch listenerState {
                case .setup:
                    print("Listener: Setup")
                case .waiting(let error):
                    print("Listener: Waiting \(error)")
                case .ready:
                    print("Listener: Ready and listens on port: \(self.udpListener?.port?.debugDescription ?? "-")")
                case .failed(let error):
                    print("Listener: Failed \(error)")
                case .cancelled:
                    print("Listener: Cancelled by myOffButton")
                    for connection in self.connections {
                        connection.cancel()
                    }
                    self.udpListener = nil
                default:
                    break;
                }
            }
            
            self.udpListener?.start(queue: backgroundQueueUdpListener)
            self.udpListener?.newConnectionHandler = { (incomingUdpConnection) in

                print ("💁 New connection \(incomingUdpConnection.debugDescription)")
                
                incomingUdpConnection.stateUpdateHandler = { (udpConnectionState) in
                    switch udpConnectionState {
                    case .setup:
                        print("Connection: setup")
                    case .waiting(let error):
                        print("Connection: waiting: \(error)")
                    case .ready:
                        print("Connection: ready")
                        self.connections.append(incomingUdpConnection)
                        self.processData(incomingUdpConnection)
                    case .failed(let error):
                        print("Connection: failed: \(error)")
                        self.connections.removeAll(where: {incomingUdpConnection === $0})
                    case .cancelled:
                        print("Connection: cancelled")
                        self.connections.removeAll(where: {incomingUdpConnection === $0})
                    default:
                        break
                    }
                }

                incomingUdpConnection.start(queue: self.backgroundQueueUdpConnection)
            }
            
        } catch {
            print("🧨")
        }
    }
    
    
    func myOffButton(_ sender: Any) {
        udpListener?.cancel()
    }
    
  
    func processData(_ incomingUdpConnection :NWConnection) {
        incomingUdpConnection.receiveMessage(completion: {(data, context, isComplete, error) in
        
            if let data = data, !data.isEmpty {
                if let string = String(data: data, encoding: .ascii) {
                    if(string == "__end__"){
                        print ("changing img")
                        self.img_data = self.img_stock
                        self.img_stock = Data()
                    }
                    else{
//                        print("img_data")
                        self.img_stock.append(data)
//                        self.img_data = data // 一回の時
                    }
                }
            }

            if error == nil {
                self.processData(incomingUdpConnection)
            }
        })
        
    }
    
   
}


struct streamView_Previews: PreviewProvider {
    static var previews: some View {
        streamView()
    }
}
