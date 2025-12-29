import React, { useState, useCallback, ReactNode } from 'react';
import { Modal } from '@components/modal/modalComponent';
import { ModalContext } from '@components/modal/modalContext';
import { ModalState, ShowModalOptions } from '@components/modal/modal.types';

export const ModalProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [modal, setModal] = useState<ModalState>({
    isOpen: false,
    title: '',
  });

  const hideModal = useCallback(() => {
    setModal((prev) => ({ ...prev, isOpen: false }));
  }, []);

  const showModal = useCallback((options: ShowModalOptions) => {
    setModal({
      ...options,
      isOpen: true,
    });
  }, []);

  return (
    <ModalContext.Provider value={{ showModal, hideModal }}>
      {children}

      <Modal
        isOpen={modal.isOpen}
        onClose={hideModal}
        title={modal.title}
        type={modal.type}
        onConfirm={modal.onConfirm}
        confirmText={modal.confirmText}
        cancelText={modal.cancelText}
        isLoading={modal.isLoading}
        width={modal.width}
      >
        {modal.content}
      </Modal>
    </ModalContext.Provider>
  );
};
