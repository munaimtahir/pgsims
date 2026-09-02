declare const beforeEach: (...args: any[]) => any;
declare const describe: (...args: any[]) => any;
declare const expect: any;
declare const it: (...args: any[]) => any;
declare const jest: any;

declare namespace jest {
  type Mock<T = any> = T;
  type MockedFunction<T = any> = T & {
    mockReset: (...args: any[]) => any;
    mockResolvedValueOnce: (...args: any[]) => any;
    mockRejectedValueOnce: (...args: any[]) => any;
    mockReturnValue: (...args: any[]) => any;
    mockImplementation: (...args: any[]) => any;
  };
}
