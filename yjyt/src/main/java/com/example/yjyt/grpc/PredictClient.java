package com.example.yjyt.grpc;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

public class PredictClient {
    ManagedChannel channel;
    PredictGrpc.PredictBlockingStub stub;

    public static void main(String[] args) {
        PredictClient client = new PredictClient();

        Result result = client.stub.predict(
                Parameter.newBuilder().setTrainId("CD17001")
                        .setDeadline("2021-10-01")
                        .build()
        );
    }

    public PredictClient() {
        channel = ManagedChannelBuilder
                .forAddress("0.0.0.0", 5000)
                .usePlaintext()
                .build();
        stub = PredictGrpc.newBlockingStub(channel);
    }
}
