module.exports = {
    testEnvironment: 'node',
    roots: ['<rootDir>/tests'],
    testMatch: [
        '**/__tests__/**/*.js',
        '**/?(*.)+(spec|test).js'
    ],
    collectCoverageFrom: [
        '*.js',
        '!jest.config.js',
        '!.eslintrc.js'
    ],
    coverageDirectory: 'coverage',
    coverageReporters: [
        'text',
        'lcov',
        'html'
    ]
};