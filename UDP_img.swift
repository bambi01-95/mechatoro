    @State var streamImg: UIImage!
    @State var boolImg: Bool = false

    
    var body: some View{
        ZStack{
            if boolImg == true{
                Image(uiImage: streamImg)
                        .resizable()
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .ignoresSafeArea()
            }

            VStack{
                Text("UDP streimng")
                Button {
                    get_img()
                } label: {
                    Image(systemName: "camera.shutter.button")
                        .resizable()
                        .frame(width:200,height: 200)
                }

            }
        }
    }
//    func send(connection: NWConnection) {
//        /* 送信データ生成 */
//        let message = "example\n"
//        let data = message.data(using: .utf8)!
//        let semaphore = DispatchSemaphore(value: 0)
//
//        /* データ送信 */
//        connection.send(content: data, completion: .contentProcessed { error in
//            if let error = error {
//                NSLog("\(#function), \(error)")
//            } else {
//                semaphore.signal()
//            }
//        })
//        /* 送信完了待ち */
//        semaphore.wait()
//    }
    
    func recv(connection: NWConnection) {
        let semaphore = DispatchSemaphore(value: 0)// なんだこれ
        // var jpg_str: type = .zero
        /* データ受信 */
        connection.receive(minimumIncompleteLength: 0,
                           maximumLength: 65535,
                           completion:{(data, context, flag, error) in
            if let error = error {
                NSLog("\(#function), \(error)")
            } else {
                // if __end__ == data {
                //      break
                //}else{
                //  img += data
                //}
                if let data = data{
                    /* 受信データのデシリアライズ */
                    print(type(of: data))
                    print(data)
                    boolImg = true
                }
                else {
                    NSLog("receiveMessage data nil")
                }
            }
        })
        /* 受信完了待ち */
        semaphore.wait()
        // image = UIImage(data: jpg_str!)
    }
    
    func disconnect(connection: NWConnection)
    {
        /* コネクション切断 */
        connection.cancel()
    }
    
    func connect(host: String, port: String) -> NWConnection
    {
        let t_host = NWEndpoint.Host(host)
        let t_port = NWEndpoint.Port(port)
        let connection : NWConnection
        let semaphore = DispatchSemaphore(value: 0)

        /* コネクションの初期化 */
        connection = NWConnection(host: t_host, port: t_port!, using: .udp)

        /* コネクションのStateハンドラ設定 */
        connection.stateUpdateHandler = { (newState) in
            switch newState {
                case .ready:
                    NSLog("Ready to receive")
                    semaphore.signal()
                case .waiting(let error):
                    NSLog("\(#function), \(error)")
                case .failed(let error):
                    NSLog("\(#function), \(error)")
                case .setup: break
                case .cancelled: break
                case .preparing: break
                @unknown default:
                    fatalError("Illegal state")
            }
        }
        
        /* コネクション開始 */
        let queue = DispatchQueue(label: "example")
        connection.start(queue:queue)

        /* コネクション完了待ち */
        semaphore.wait()
        return connection
    }
    
    func get_img()
    {
        let connection : NWConnection
        let host = "172.20.10.7"
        let port = "8080"
        
        /* コネクション開始 */
        connection = connect(host: host, port: port)
        /* データ送信 */
//        send(connection: connection)
        /* データ受信 */
        recv(connection: connection)
        /* コネクション切断 */
        disconnect(connection: connection)
    }