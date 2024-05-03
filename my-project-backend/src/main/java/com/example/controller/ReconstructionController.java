package com.example.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.scheduling.annotation.Async;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.http.ResponseEntity;
import java.util.Map;
import java.util.HashMap;
import org.springframework.http.HttpStatus;



@RestController
@RequestMapping("/api/reconstruction")
public class ReconstructionController {

    @PostMapping("/start")
    public ResponseEntity<Map<String, Object>> startReconstruction() {
        try {
            Thread.sleep(1000);
            Map<String, Object> result = new HashMap<>();
            result.put("code", 200);
            result.put("message", "重建成功");
            return ResponseEntity.ok(result);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            Map<String, Object> errorResult = new HashMap<>();
            errorResult.put("code", 500);
            errorResult.put("message", "重建过程中发生错误");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResult);
        }
    }
}


