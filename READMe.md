# Distritbuted Hash Table (DHT) Implementation in Python with TCP Client-Server Architecture

## Introduction
This is a simple implementation of a Distributed Hash Table (DHT) in Python using TCP Client-Server Architecture. The DHT is a distributed system that provides a lookup service similar to a hash table: (key, value) pairs are stored in the DHT, and any participating node can efficiently retrieve the value associated with a given key. Responsibility for maintaining the mapping from keys to values is distributed among the nodes, in such a way that a change in the set of participants causes a minimal amount of disruption. This allows a DHT to scale to extremely large numbers of nodes and to handle continual node arrivals, departures, and failures.

Here i also try to implement a resp_parser that can parse RESP (REdis Serialization Protocol) messages. The RESP is a binary-safe protocol, this means that you can use it to handle strings containing any kind of data, including raw binary data. This is a fundamental feature of Redis, so important that the protocol is sometimes called RESP2, where the 2 means “binary safe”.

## How to run
1. Clone the repository
2. Run the tcp_api.py file passing the ports numbers as an argument
3. Run the client.py file passing the port number as an argument, can choose any port number from the one used in step 2
4. Parse the comands

 # Not finished yet
