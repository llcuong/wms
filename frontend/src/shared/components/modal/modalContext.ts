import { createContext } from 'react';
import { ModalContextType } from '@components/modal/modal.types';

export const ModalContext = createContext<ModalContextType | undefined>(undefined);
