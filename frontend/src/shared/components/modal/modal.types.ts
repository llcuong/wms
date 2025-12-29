import { ReactNode } from 'react';

export type ModalType = 'success' | 'error' | 'warning' | 'info' | 'confirm' | 'default';

export interface ShowModalOptions {
  type?: ModalType;
  title: string;
  content?: ReactNode;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
  isLoading?: boolean;
  width?: string;
}

export interface ModalState extends ShowModalOptions {
  isOpen: boolean;
}

export interface ModalContextType {
  showModal: (options: ShowModalOptions) => void;
  hideModal: () => void;
}
