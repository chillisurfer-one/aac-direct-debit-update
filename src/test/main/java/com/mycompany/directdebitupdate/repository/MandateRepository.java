package com.mycompany.directdebitupdate.repository;

import com.mycompany.directdebitupdate.domain.Mandate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MandateRepository extends JpaRepository<Mandate, Long> {
    Optional<Mandate> findByMandateId(String mandateId);
}