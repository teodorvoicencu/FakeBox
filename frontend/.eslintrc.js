module.exports = {
  env: {
    es6: true,
    node: true,
    jest: true,
  },
  extends: [
    'airbnb',
    'plugin:@typescript-eslint/recommended',
    'prettier',
    'plugin:prettier/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
      impliedStrict: true,
    },
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: ['react', 'react-hooks', 'import'],
  settings: {
    'import/parsers': {
      '@typescript-eslint/parser': ['.ts', '.tsx'],
    },
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        paths: './tsconfig.json',
      },
      node: {
        extensions: ['.js', '.jsx', 'ts', '.tsx'],
      },
    },
  },
  globals: {
    __DEV__: true,
  },
  rules: {
    'global-require': 0,
    'linebreak-style': [2, 'unix'],
    'prefer-const': 0,
    'no-console': [
      'warn',
      {
        allow: ['warn', 'error', 'log', 'info', 'disableYellowBox'],
      },
    ],
    'no-param-reassign': ['error', { props: false }],
    'no-restricted-globals': 0,
    'no-unused-vars': 0,
    'no-use-before-define': 0,
    'no-underscore-dangle': 0,
    'no-useless-constructor': 0,
    'no-unused-expressions': 0,
    'no-plusplus': 0,
    'no-nested-ternary': 0,
    'lines-between-class-members': [
      1,
      'always',
      {
        exceptAfterSingleLine: true,
      },
    ],
    'prefer-destructuring': [
      2,
      {
        array: false,
        object: true,
      },
    ],
    'max-classes-per-file': 0,
    'react-hooks/rules-of-hooks': 'error', // Checks rules of Hooks
    'react-hooks/exhaustive-deps': 'error', // Checks effect dependencies
    'import/prefer-default-export': 0,
    'react/prefer-stateless-function': 0,
    'react/destructuring-assignment': 0,
    'react/prop-types': 0,
    'react/react-in-jsx-scope': 0,
    'react/jsx-props-no-spreading': 0,
    'react/no-array-index-key': 0,
    'react/require-default-props': 0,
    'react/jsx-filename-extension': [
      2,
      {
        extensions: ['.jsx', '.tsx'],
      },
    ],
    'jsx-a11y/accessible-emoji': 0,
    'react/static-property-placement': 0,
    'import/no-extraneous-dependencies': [
      'error',
      {
        devDependencies: true,
        optionalDependencies: false,
        peerDependencies: false,
      },
    ],
    '@typescript-eslint/explicit-member-accessibility': [
      2,
      { accessibility: 'no-public' },
    ],
    '@typescript-eslint/no-empty-interface': 1,
    '@typescript-eslint/explicit-function-return-type': [
      0,
      {
        allowExpressions: true,
        allowTypedFunctionExpressions: true,
      },
    ],
    '@typescript-eslint/no-explicit-any': 0,
    '@typescript-eslint/no-use-before-define': [
      2,
      {
        functions: true,
        classes: true,
        variables: false,
      },
    ],
    '@typescript-eslint/no-unused-vars': [1, { args: 'none' }],
    '@typescript-eslint/no-non-null-assertion': 0,
    '@typescript-eslint/camelcase': 0,
    '@typescript-eslint/ban-ts-ignore': 0,
    '@typescript-eslint/no-var-requires': 0,
    'import/extensions': [
      'error',
      'ignorePackages',
      {
        js: 'never',
        jsx: 'never',
        ts: 'never',
        tsx: 'never',
      },
    ],
    'no-shadow': 'off',
    '@typescript-eslint/no-shadow': ['error'],
  },
};
