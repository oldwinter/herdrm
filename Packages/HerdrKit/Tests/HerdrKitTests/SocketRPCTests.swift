import Darwin
import Foundation
import XCTest
@testable import HerdrKit

final class SocketRPCTests: XCTestCase {
    func testConnectDisablesSIGPIPE() throws {
        // Names stay short because sockaddr_un caps paths at 104 bytes and
        // temporaryDirectory already burns most of that (/var/folders/…).
        let directory = FileManager.default.temporaryDirectory
            .appendingPathComponent("hk-\(UUID().uuidString.prefix(8))", isDirectory: true)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: directory) }

        let path = directory.appendingPathComponent("s.sock").path
        let listener = socket(AF_UNIX, SOCK_STREAM, 0)
        XCTAssertGreaterThanOrEqual(listener, 0)
        defer { close(listener) }

        var address = sockaddr_un()
        address.sun_family = sa_family_t(AF_UNIX)
        let pathBytes = Array(path.utf8)
        XCTAssertLessThan(pathBytes.count, MemoryLayout.size(ofValue: address.sun_path))
        withUnsafeMutableBytes(of: &address.sun_path) { raw in
            raw.copyBytes(from: pathBytes)
        }
        let addressLength = socklen_t(MemoryLayout<sockaddr_un>.size)
        let bindResult = withUnsafePointer(to: &address) { pointer in
            pointer.withMemoryRebound(to: sockaddr.self, capacity: 1) { socketAddress in
                Darwin.bind(listener, socketAddress, addressLength)
            }
        }
        XCTAssertEqual(bindResult, 0, String(cString: strerror(errno)))
        XCTAssertEqual(listen(listener, 1), 0, String(cString: strerror(errno)))

        let client = try SocketRPC.connect(path: path)
        defer { close(client) }

        var noSigPipe: Int32 = 0
        var optionLength = socklen_t(MemoryLayout.size(ofValue: noSigPipe))
        XCTAssertEqual(
            getsockopt(client, SOL_SOCKET, SO_NOSIGPIPE, &noSigPipe, &optionLength),
            0,
            String(cString: strerror(errno))
        )
        XCTAssertEqual(noSigPipe, 1)
    }

    func testClearsPriorReceiveTimeoutForBlockingReads() throws {
        var sockets = [Int32](repeating: -1, count: 2)
        XCTAssertEqual(socketpair(AF_UNIX, SOCK_STREAM, 0, &sockets), 0)
        defer {
            close(sockets[0])
            close(sockets[1])
        }

        try SocketRPC.configureReadTimeout(fd: sockets[0], timeoutSeconds: 15)
        XCTAssertEqual(try receiveTimeout(fd: sockets[0]).tv_sec, 15)

        try SocketRPC.configureReadTimeout(fd: sockets[0], timeoutSeconds: nil)
        let cleared = try receiveTimeout(fd: sockets[0])
        XCTAssertEqual(cleared.tv_sec, 0)
        XCTAssertEqual(cleared.tv_usec, 0)
    }

    func testSubscribeAckErrorsAreNotAccepted() throws {
        let line = Data(#"{"error":{"code":"denied","message":"no access"}}"#.utf8)
        XCTAssertThrowsError(try SocketRPC.decodeResponse(line)) { error in
            guard case HerdrError.rpc(let code, let message) = error else {
                return XCTFail("expected RPC error, got \(error)")
            }
            XCTAssertEqual(code, "denied")
            XCTAssertEqual(message, "no access")
        }
    }

    func testMalformedEventIsAProtocolError() {
        XCTAssertThrowsError(try SocketRPC.decodeEvent(Data("not json".utf8))) { error in
            guard case HerdrError.malformedResponse(let reason) = error else {
                return XCTFail("expected malformed response, got \(error)")
            }
            XCTAssertEqual(reason, "undecodable event")
        }
    }

    func testEventDecoderPreservesValidPayloadAndKind() throws {
        let event = try SocketRPC.decodeEvent(
            Data(#"{"event":{"type":"agent.updated"},"value":7}"#.utf8)
        )
        XCTAssertEqual(event.kind, "agent.updated")
        XCTAssertEqual(event.payload["value"], .number(7))
    }

    func testNDJSONLineLimitAllowsBoundaryAndRejectsOverflow() {
        XCTAssertNoThrow(try SocketRPC.validateLineLength(SocketRPC.maximumLineBytes))
        XCTAssertThrowsError(
            try SocketRPC.validateLineLength(SocketRPC.maximumLineBytes + 1)
        )
    }

    private func receiveTimeout(fd: Int32) throws -> timeval {
        var timeout = timeval()
        var length = socklen_t(MemoryLayout<timeval>.size)
        guard getsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, &length) == 0 else {
            throw NSError(
                domain: NSPOSIXErrorDomain,
                code: Int(errno),
                userInfo: nil
            )
        }
        return timeout
    }
}
