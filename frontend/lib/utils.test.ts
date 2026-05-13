/// <reference types="jest" />
import { downloadFile } from './utils';

describe('utils', () => {
  describe('downloadFile', () => {
    let appendChildSpy: jest.SpyInstance;
    let removeChildSpy: jest.SpyInstance;

    beforeEach(() => {
      // Mock URL methods
      if (typeof window.URL.createObjectURL === 'undefined') {
        Object.defineProperty(window.URL, 'createObjectURL', { value: jest.fn() });
      }
      if (typeof window.URL.revokeObjectURL === 'undefined') {
        Object.defineProperty(window.URL, 'revokeObjectURL', { value: jest.fn() });
      }

      (window.URL.createObjectURL as jest.Mock).mockReturnValue('blob:url');
      (window.URL.revokeObjectURL as jest.Mock).mockImplementation(() => {});
      
      appendChildSpy = jest.spyOn(document.body, 'appendChild').mockImplementation(() => ({} as unknown as Node));
      removeChildSpy = jest.spyOn(document.body, 'removeChild').mockImplementation(() => ({} as unknown as Node));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    it('triggers a file download', () => {
      const blob = new Blob(['content'], { type: 'text/plain' });
      const filename = 'test.txt';

      downloadFile(blob, filename);

      expect(window.URL.createObjectURL).toHaveBeenCalledWith(blob);
      expect(appendChildSpy).toHaveBeenCalled();
      expect(removeChildSpy).toHaveBeenCalled();
      expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:url');
    });
  });
});
