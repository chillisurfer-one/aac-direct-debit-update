package com.mycompany.directdebitupdate.service;

import com.mycompany.directdebitupdate.dto.DirectDebitUpdateRequest;
import com.mycompany.directdebitupdate.domain.Mandate;
import com.mycompany.directdebitupdate.repository.MandateRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MandateService {

    private static final Logger log = LoggerFactory.getLogger(MandateService.class);

    private final MandateRepository repository;

    @Transactional
    public void updateMandate(DirectDebitUpdateRequest request) {
        log.info("Updating mandate: {}", request.getMandateId());

        Mandate mandate = repository.findByMandateId(request.getMandateId())
                .orElseThrow(() -> new IllegalArgumentException("Mandate not found"));

        mandate.setAccountNumber(request.getAccountNumber());
        mandate.setSortCode(request.getSortCode());
        mandate.setUpdatedBy(request.getUpdatedBy());
        mandate.setStatus("UPDATED");

        repository.save(mandate);
    }
}