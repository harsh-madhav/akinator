import { useState, useEffect } from "react";
import { startGame, answerQuestion } from "./api";

function App() {
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [currentQuestion, setCurrentQuestion] = useState<string>("");
    const [isGuessing, setIsGuessing] = useState<boolean>(false);
    const [guess, setGuess] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [gameOver, setGameOver] = useState<boolean>(false);
    const [gameSuccess, setGameSuccess] = useState<boolean>(false);

    // Start a new game
    const startNewGame = async () => {
        try {
            setIsLoading(true);
            const { session_id, question } = await startGame();
            setSessionId(session_id);
            setCurrentQuestion(question);
            setIsGuessing(false);
            setGameOver(false);
            setGuess("");
        } catch (error) {
            console.error("Error starting game:", error);
        } finally {
            setIsLoading(false);
        }
    };

    // Handle user's answer
    const handleAnswer = async (answer: string) => {
        if (!sessionId || isLoading) return;
        
        try {
            setIsLoading(true);
            const isFeedback = isGuessing;
            const response = await answerQuestion(sessionId, answer, isFeedback);
            
            if (response.game_over) {
                setCurrentQuestion(response.message);
                setGameOver(true);
                setGameSuccess(response.success || false);
                setIsGuessing(false);
            } else if (response.is_guess) {
                setGuess(response.message);
                setIsGuessing(true);
            } else {
                setCurrentQuestion(response.message);
                setIsGuessing(false);
            }
        } catch (error) {
            console.error("Error answering question:", error);
        } finally {
            setIsLoading(false);
        }
    };

    // Start a new game when component mounts
    useEffect(() => {
        startNewGame();
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
            <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
                <h1 className="text-2xl font-bold text-center mb-6">
                    {gameOver && gameSuccess ? '🎉 Congratulations! 🎉' : 'Akinator Game'}
                </h1>
                
                {isLoading ? (
                    <div className="text-center py-8">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                        <p className="mt-2 text-gray-600">Thinking...</p>
                    </div>
                ) : gameOver ? (
                    <div className="text-center">
                        <div className="mb-6">
                            {gameSuccess ? (
                                <div className="text-green-600 mb-4">
                                    <svg className="w-16 h-16 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                            ) : null}
                            <p className="text-lg">{currentQuestion}</p>
                        </div>
                        <div className="flex justify-center">
                            <button
                                onClick={startNewGame}
                                className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                            >
                                Play Again
                            </button>
                        </div>
                    </div>
                ) : isGuessing ? (
                    <div className="text-center">
                        <p className="text-lg mb-4">{guess}</p>
                        <div className="flex justify-center space-x-4 mt-6">
                            <button
                                onClick={() => handleAnswer("Yes")}
                                className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                                disabled={isLoading}
                            >
                                Yes
                            </button>
                            <button
                                onClick={() => handleAnswer("No")}
                                className="px-6 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                disabled={isLoading}
                            >
                                No
                            </button>
                        </div>
                    </div>
                ) : (
                    <div>
                        <p className="text-lg mb-6">{currentQuestion}</p>
                        <div className="flex justify-center space-x-4">
                            <button
                                onClick={() => handleAnswer("Yes")}
                                className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                                disabled={isLoading}
                            >
                                Yes
                            </button>
                            <button
                                onClick={() => handleAnswer("No")}
                                className="px-6 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                disabled={isLoading}
                            >
                                No
                            </button>
                            <button
                                onClick={() => handleAnswer("Maybe")}
                                className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                                disabled={isLoading}
                            >
                                Maybe
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;