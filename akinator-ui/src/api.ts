import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export interface StartGameResponse {
    session_id: string;
    question: string;
}

export interface AnswerResponse {
    message: string;
    is_guess: boolean;
    confidence?: number;
    game_over?: boolean;
    success?: boolean;
}

export const startGame = async (): Promise<StartGameResponse> => {
    const response = await axios.post<StartGameResponse>(`${API_BASE}/start`);
    return response.data;
};

export const answerQuestion = async (
    sessionId: string,
    answer: string,
    isFeedback: boolean = false
): Promise<AnswerResponse> => {
    const response = await axios.post<AnswerResponse>(`${API_BASE}/answer`, {
        session_id: sessionId,
        answer,
        is_feedback: isFeedback
    });
    return response.data;
};