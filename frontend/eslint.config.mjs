import coreWebVitals from 'eslint-config-next/core-web-vitals';
import typescript from 'eslint-config-next/typescript';

export default [
  ...coreWebVitals,
  ...typescript,
  {
    linterOptions: {
      reportUnusedDisableDirectives: 'off',
    },
    rules: {
      // Preserve the existing Next 14 lint baseline while upgrading the
      // framework. These React Compiler diagnostics are not enabled by the
      // application's current runtime configuration.
      'react-hooks/immutability': 'off',
      'react-hooks/preserve-manual-memoization': 'off',
      'react-hooks/purity': 'off',
      'react-hooks/set-state-in-effect': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-require-imports': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      'import/no-anonymous-default-export': 'off',
      '@next/next/no-location-assign-relative-destination': 'off',
    },
  },
];
