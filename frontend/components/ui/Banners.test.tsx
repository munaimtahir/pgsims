import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorBanner from './ErrorBanner';
import SuccessBanner from './SuccessBanner';

describe('Banner components', () => {
  describe('ErrorBanner', () => {
    it('renders message and details', () => {
      render(<ErrorBanner message="Failed" details="Invalid input" />);
      expect(screen.getByText('Failed')).toBeInTheDocument();
      expect(screen.getByText('Invalid input')).toBeInTheDocument();
    });

    it('handles dismiss click', () => {
      const onDismiss = jest.fn();
      render(<ErrorBanner message="Failed" onDismiss={onDismiss} />);
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      
      expect(onDismiss).toHaveBeenCalledTimes(1);
    });
  });

  describe('SuccessBanner', () => {
    it('renders message', () => {
      render(<SuccessBanner message="Saved successfully" />);
      expect(screen.getByText('Saved successfully')).toBeInTheDocument();
    });

    it('handles dismiss click', () => {
      const onDismiss = jest.fn();
      render(<SuccessBanner message="Saved" onDismiss={onDismiss} />);
      
      const button = screen.getByRole('button');
      fireEvent.click(button);
      
      expect(onDismiss).toHaveBeenCalledTimes(1);
    });
  });
});
