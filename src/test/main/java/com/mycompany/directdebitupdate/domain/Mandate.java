package com.mycompany.directdebitupdate.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "direct_debit_mandate")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Mandate {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String mandateId;
    private String accountNumber;
    private String sortCode;
    private String updatedBy;
    private String status;
}