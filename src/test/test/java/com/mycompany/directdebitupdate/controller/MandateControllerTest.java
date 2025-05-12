package com.mycompany.directdebitupdate.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mycompany.directdebitupdate.dto.DirectDebitUpdateRequest;
import com.mycompany.directdebitupdate.service.MandateService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(MandateController.class)
public class MandateControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MandateService service;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldUpdateMandate() throws Exception {
        DirectDebitUpdateRequest request = new DirectDebitUpdateRequest();
        request.setMandateId("MAND123");
        request.setAccountNumber("12345678");
        request.setSortCode("12-34-56");
        request.setUpdatedBy("system");

        mockMvc.perform(put("/api/v1/mandates/update")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk());

        Mockito.verify(service).updateMandate(Mockito.any());
    }
}