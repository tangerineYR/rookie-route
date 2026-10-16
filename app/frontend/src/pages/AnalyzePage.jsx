import { apiFetch } from "../lib/api";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import ErrorPatternCard from "../components/ErrorPatternCard";
import ErrorTypeChart from "../components/ErrorTypeChart";
import StatisticsCard from "../components/StatisticsCard";

const AnalyzePage = () => {
    const [history, setHistory] = useState([]);
    const [dashboardData, setDashboardData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [userId, setUserId] = useState("");
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    // Check login status
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const storedUsername = localStorage.getItem('username');

        if (token && storedUsername) {
            setIsLoggedIn(true);
            setUserId(storedUsername);
        } else {
            setIsLoggedIn(false);
            setLoading(false);
        }
    }, []);

    // Load dashboard data from backend
    useEffect(() => {
        if (!userId) return;

        const fetchDashboardData = async () => {
            try {
                setLoading(true);
                setError(null);
                const res = await apiFetch("/dashboard/stats/me", { authenticated: true });

                if (res.status === 401) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('username');
                    setDashboardData(null);
                    setIsLoggedIn(false);
                    return;
                }
                if (!res.ok) throw new Error('통계를 불러오지 못했습니다. 다시 시도해주세요.');
                if (res.ok) {
                    const data = await res.json();
                    setDashboardData(data);
                }
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, [userId]);

    // Load history from localStorage
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

    // Real data from backend (no mock data)

    // Calculate statistics from real data
    const totalAnalyses = dashboardData?.total_submissions || 0;

    // Convert backend stats to chart data
    const errorTypeData = dashboardData?.stats?.length > 0
        ? dashboardData.stats.map(stat => ({
            name: stat.weakness_type,
            value: stat.count
        }))
        : [];

    // Calculate error patterns from backend data
    const errorPatterns = dashboardData?.stats?.length > 0
        ? dashboardData.stats.map((stat, index) => {
            const totalErrors = dashboardData.stats.reduce((sum, s) => sum + s.count, 0);
            const percentage = (stat.count / totalErrors) * 100;
            let severity = "low";
            if (percentage > 30) severity = "high";
            else if (percentage > 15) severity = "medium";

            return {
                pattern: stat.weakness_type,
                count: stat.count,
                percentage: percentage,
                severity: severity
            };
        })
        : [];

    // 가장 흔한 오류 패턴
    const mostCommonError = errorPatterns.length > 0 ? errorPatterns[0].pattern : "없음";

    // 로그인하지 않은 경우 로그인 유도 화면
    if (!isLoggedIn) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center px-4">
                <div className="max-w-md w-full text-center">
                    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
                        <div className="mb-6">
                            <svg className="w-20 h-20 mx-auto text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                        </div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                            로그인이 필요합니다
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400 mb-8">
                            코드 분석 리포트를 확인하려면 로그인해주세요.
                        </p>
                        <div className="space-y-3">
                            <Link
                                to="/login"
                                className="block w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                            >
                                로그인하기
                            </Link>
                            <Link
                                to="/signup"
                                className="block w-full px-6 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                            >
                                회원가입하기
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                {/* Page Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                        코드 분석 리포트
                    </h1>
                    <p className="text-lg text-gray-600 dark:text-gray-400">
                        당신의 코딩 패턴을 분석하고 개선 방향을 제시합니다
                    </p>
                </div>

                {error && <p role="alert" className="text-red-600 mb-6">{error}</p>}
                {/* 3번 기능: Personal Error Pattern Analysis */}
                <div className="mb-16">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                        개인 오류 패턴 분석
                    </h2>

                    {loading ? (
                        <div className="text-center py-8">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                            <p className="mt-4 text-gray-600 dark:text-gray-400">데이터를 불러오는 중...</p>
                        </div>
                    ) : errorPatterns.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {errorPatterns.map((pattern, index) => (
                                <ErrorPatternCard
                                    key={index}
                                    pattern={pattern.pattern}
                                    count={pattern.count}
                                    percentage={pattern.percentage}
                                    severity={pattern.severity}
                                />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-700">
                            <svg className="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <p className="mt-4 text-gray-600 dark:text-gray-400">아직 분석 데이터가 없습니다.</p>
                            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">코드를 분석하면 여기에 패턴이 표시됩니다.</p>
                        </div>
                    )}
                </div>

                {/* 4번 기능: Code Improvement Report Visualization */}
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                        코드 개선 리포트
                    </h2>

                    {/* Statistics Cards */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                        <StatisticsCard
                            icon={
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                            }
                            title="총 분석 횟수"
                            value={totalAnalyses}
                            subtitle="코드 분석 완료"
                            color="blue"
                        />
                        <StatisticsCard
                            icon={
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            }
                            title="주요 오류"
                            value={mostCommonError}
                            subtitle="가장 빈번한 패턴"
                            color="red"
                        />
                    </div>

                    {/* Charts */}
                    {errorTypeData.length > 0 ? (
                        <ErrorTypeChart data={errorTypeData} />
                    ) : (
                        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-700">
                            <svg className="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            <p className="mt-4 text-gray-600 dark:text-gray-400">아직 분석 데이터가 없습니다.</p>
                            <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">코드를 분석하면 오류 통계가 표시됩니다.</p>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <footer className="mt-16 text-center text-gray-600 dark:text-gray-400 text-sm">
                    <p>데이터는 서버에 안전하게 저장되며, 실시간으로 업데이트됩니다.</p>
                </footer>
            </div>
        </div>
    );
};

export default AnalyzePage;
