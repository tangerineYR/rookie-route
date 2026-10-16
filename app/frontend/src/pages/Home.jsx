import { apiFetch, apiErrorMessage } from "../lib/api";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import CodeEditor from "../components/CodeEditor";
import LoadingSpinner from "../components/LoadingSpinner";
import AnalysisResult from "../components/AnalysisResult";
import HistoryPanel from "../components/HistoryPanel";
import CodeExamples from "../components/CodeExamples";

const Home = () => {
    const [code, setCode] = useState("");
    const [language, setLanguage] = useState("javascript");
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();

    // Load history from localStorage on mount
    useEffect(() => {
        const savedHistory = localStorage.getItem('analysisHistory');
        if (savedHistory) {
            try {
                setHistory(JSON.parse(savedHistory));
            } catch (e) {
                console.error('Failed to load history:', e);
            }
        }
    }, []);

    // Save history to localStorage whenever it changes
    useEffect(() => {
        if (history.length > 0) {
            localStorage.setItem('analysisHistory', JSON.stringify(history));
        }
    }, [history]);

    const analyzeCode = async () => {
        if (!code.trim()) {
            setError("Please enter some code to analyze");
            return;
        }

        // JWT 토큰 확인
        const token = localStorage.getItem('access_token');
        if (!token) {
            setError("로그인이 필요합니다.");
            setTimeout(() => navigate('/login'), 2000);
            return;
        }

        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const res = await apiFetch("/review/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    code: code,
                    language: language
                })
            });

            if (!res.ok) {
                const errorData = await res.json().catch(() => ({}));

                // 401 Unauthorized - 토큰이 유효하지 않음
                if (res.status === 401) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('username');
                    setError("로그인이 만료되었습니다. 다시 로그인해주세요.");
                    setTimeout(() => navigate('/login'), 2000);
                    return;
                }

                throw new Error(apiErrorMessage(errorData, `Server error: ${res.status}`));
            }

            const data = await res.json();

            // Format analysis result for display
            let formattedResult = `## ${data.summary}\n\n`;

            if (data.weaknesses && data.weaknesses.length > 0) {
                formattedResult += `### 발견된 문제점:\n\n`;
                data.weaknesses.forEach((weakness, index) => {
                    formattedResult += `**${index + 1}. ${weakness.type}** (Line ${weakness.line})\n`;
                    formattedResult += `${weakness.explanation}\n\n`;
                });
            } else {
                formattedResult += `✅ 문제점이 발견되지 않았습니다!`;
            }

            setResult(formattedResult);

            // Add to history
            const historyItem = {
                id: Date.now(),
                submission_id: data.submission_id,
                code: code,
                language: language,
                result: formattedResult,
                timestamp: Date.now()
            };

            setHistory(prev => [historyItem, ...prev].slice(0, 20)); // Keep last 20 items
        } catch (err) {
            setError(err.message || "Failed to analyze code. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleLoadHistory = (item) => {
        setCode(item.code);
        setLanguage(item.language);
        setResult(item.result);
        setError(null);
    };

    const handleClearHistory = () => {
        if (window.confirm('Are you sure you want to clear all history?')) {
            setHistory([]);
            localStorage.removeItem('analysisHistory');
        }
    };

    const handleLoadExample = (exampleCode) => {
        setCode(exampleCode);
        setResult(null);
        setError(null);
    };

    // 로그인 여부 확인
    const isLoggedIn = !!localStorage.getItem('access_token');

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-200">
            {/* History Panel - 로그인한 경우만 표시 */}
            {isLoggedIn && (
                <HistoryPanel
                    history={history}
                    onLoadHistory={handleLoadHistory}
                    onClearHistory={handleClearHistory}
                />
            )}

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
                <div className="space-y-6">
                    {/* Code Editor */}
                    <CodeEditor
                        code={code}
                        setCode={setCode}
                        language={language}
                        setLanguage={setLanguage}
                        disabled={isLoading}
                    />

                    {/* Action Buttons */}
                    <div className="flex flex-col sm:flex-row justify-center gap-3">
                        <button
                            onClick={analyzeCode}
                            disabled={isLoading || !code.trim()}
                            className="w-full sm:w-auto px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
                        >
                            {isLoading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span>Analyzing...</span>
                                </>
                            ) : (
                                <>
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                    </svg>
                                    <span>Analyze My Code</span>
                                </>
                            )}
                        </button>

                        <CodeExamples
                            language={language}
                            onLoadExample={handleLoadExample}
                        />
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900 dark:bg-opacity-30 border-l-4 border-red-500 rounded-lg p-4 shadow-md animate-shake">
                            <div className="flex items-start">
                                <svg className="w-6 h-6 text-red-500 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <div>
                                    <h3 className="text-red-800 dark:text-red-200 font-semibold">Error</h3>
                                    <p className="text-red-700 dark:text-red-300 mt-1">{error}</p>
                                </div>
                                <button
                                    onClick={() => setError(null)}
                                    className="ml-auto text-red-500 hover:text-red-700 dark:hover:text-red-400 transition-colors"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Loading Spinner */}
                    {isLoading && <LoadingSpinner message="Analyzing your code..." />}

                    {/* Analysis Result */}
                    {result && !isLoading && (
                        <AnalysisResult
                            result={result}
                            onClear={() => setResult(null)}
                        />
                    )}
                </div>
            </main>

            {/* Footer */}
            <footer className="mt-12 pb-8 text-center text-gray-600 dark:text-gray-400 text-sm">
                <p>Built with React, Tailwind CSS & Monaco Editor</p>
            </footer>
        </div>
    );
};

export default Home;
