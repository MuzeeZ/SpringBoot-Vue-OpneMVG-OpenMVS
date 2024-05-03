package com.example.controller;

import lombok.Getter;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpStatus;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.*;
import java.util.Objects;

@RestController
public class FileUploadController {

    private final Path rootLocation = Paths.get("videos");

    @PostMapping("/upload")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file) {
        try {
            Files.createDirectories(this.rootLocation);
            if (file.isEmpty()) {
                return ResponseEntity.badRequest().body(
                        new ApiResponse(400, "Failed to store empty file")
                );
            }
            Path destinationFile = this.rootLocation.resolve(
                            Paths.get(Objects.requireNonNull(file.getOriginalFilename())))
                    .normalize().toAbsolutePath();
            if (!destinationFile.getParent().equals(this.rootLocation.toAbsolutePath())) {
                return ResponseEntity.badRequest().body(
                        new ApiResponse(400, "Cannot store file outside current directory")
                );
            }
            try (var inputStream = file.getInputStream()) {
                Files.copy(inputStream, destinationFile, StandardCopyOption.REPLACE_EXISTING);
                return ResponseEntity.ok(
                        new ApiResponse(200, "File uploaded successfully: " + file.getOriginalFilename())
                );
            }
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
                    new ApiResponse(500, "Failed to upload file: " + e.getMessage())
            );
        }
    }

    @GetMapping("/videos/{filename:.+}")
    public ResponseEntity<?> serveFile(@PathVariable String filename) {
        try {
            Path file = rootLocation.resolve(filename);
            Resource resource = new UrlResource(file.toUri());
            if (resource.exists() || resource.isReadable()) {
                return ResponseEntity.ok().header("Content-Disposition", "attachment; filename=\"" + resource.getFilename() + "\"").body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException e) {
            return ResponseEntity.badRequest().body(
                    new ApiResponse(400, "Could not read file: " + filename)
            );
        }
    }

    @Getter
    static class ApiResponse {
        private int code;
        private String message;

        public ApiResponse(int code, String message) {
            this.code = code;
            this.message = message;
        }

    }
}

