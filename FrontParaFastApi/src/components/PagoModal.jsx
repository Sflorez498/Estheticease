import React, { useState } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';

const PagoModal = ({ show, handleClose, handlePago }) => {
  const [numeroTarjeta, setNumeroTarjeta] = useState('');
  const [clave, setClave] = useState('');
  const [error, setError] = useState('');
  const [exito, setExito] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    
    // Validar número de tarjeta (10 dígitos)
    if (!/^[0-9]{10}$/.test(numeroTarjeta)) {
      setError('El número de tarjeta debe tener exactamente 10 dígitos');
      return;
    }

    // Validar clave (al menos 4 caracteres)
    if (clave.length < 4) {
      setError('La clave debe tener al menos 4 caracteres');
      return;
    }

    // Simular pago exitoso
    setExito(true);
    setTimeout(() => {
      handlePago();
      handleClose();
    }, 1500);
  };

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Pago</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {exito ? (
          <Alert variant="success">
            ¡Compra exitosa! Los productos han sido eliminados del carrito.
          </Alert>
        ) : (
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Número de tarjeta</Form.Label>
              <Form.Control
                type="text"
                placeholder="1234567890"
                value={numeroTarjeta}
                onChange={(e) => setNumeroTarjeta(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Clave</Form.Label>
              <Form.Control
                type="password"
                placeholder="Clave"
                value={clave}
                onChange={(e) => setClave(e.target.value)}
              />
            </Form.Group>
            {error && <Alert variant="danger">{error}</Alert>}
            <Button variant="primary" type="submit" className="w-100">
              Pagar
            </Button>
          </Form>
        )}
      </Modal.Body>
    </Modal>
  );
};

export default PagoModal;
