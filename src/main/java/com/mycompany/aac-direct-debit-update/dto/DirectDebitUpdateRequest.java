package com.mycompany.directdebitupdate.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class DirectDebitUpdateRequest {

    @NotBlank(message = "Mandate ID is required")
    private String mandateId;

    @NotBlank(message = "Account number is required")
    private String accountNumber;

    @NotBlank(message = "Sort code is required")
    private String sortCode;

    private String updatedBy;
}