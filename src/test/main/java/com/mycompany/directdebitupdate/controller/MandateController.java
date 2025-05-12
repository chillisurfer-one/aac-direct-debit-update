package com.mycompany.directdebitupdate.controller;

import com.mycompany.directdebitupdate.dto.DirectDebitUpdateRequest;
import com.mycompany.directdebitupdate.service.MandateService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/mandates")
@RequiredArgsConstructor
public class MandateController {

    private static final Logger log = LoggerFactory.getLogger(MandateController.class);

    private final MandateService service;

    @PutMapping("/update")
    public ResponseEntity<String> updateMandate(@RequestBody @Valid DirectDebitUpdateRequest request) {
        log.info("Received update request for mandate: {}", request.getMandateId());
        service.updateMandate(request);
        return ResponseEntity.ok("Mandate updated successfully");
    }
}