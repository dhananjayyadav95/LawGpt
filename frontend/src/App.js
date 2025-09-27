import React, { useState, useEffect } from 'react';
import './App.css';
import { Button } from './components/ui/button';
import { Textarea } from './components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { Separator } from './components/ui/separator';
import { ScrollArea } from './components/ui/scroll-area';
import { Scale, BookOpen, FileText, AlertTriangle, Clock } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [query, setQuery] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [userSession] = useState(() => {
    const stored = localStorage.getItem('nepal-law-session');
    if (stored) return stored;
    const newSession = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('nepal-law-session', newSession);
    return newSession;
  });

  // Load history on component mount
  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await axios.get(`${API}/legal-history/${userSession}`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const analyzeQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/analyze-legal-problem`, {
        query_text: query,
        user_session: userSession
      });
      
      setAnalysis(response.data);
      setQuery('');
      loadHistory(); // Refresh history
    } catch (error) {
      console.error('Error analyzing legal problem:', error);
      alert('Error analyzing your legal problem. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatDateTime = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatResponse = (text) => {
    // Simple formatting for better readability
    return text
      .split('\n')
      .map((line, index) => {
        if (line.includes('**') || line.includes('##')) {
          return <h3 key={index} className="font-semibold text-lg mt-4 mb-2 text-slate-800">{line.replace(/[*#]/g, '')}</h3>;
        }
        if (line.trim().startsWith('-') || line.trim().startsWith('•')) {
          return <li key={index} className="ml-4 text-slate-700">{line.replace(/^[-•]\s*/, '')}</li>;
        }
        if (line.trim()) {
          return <p key={index} className="mb-2 text-slate-700 leading-relaxed">{line}</p>;
        }
        return <br key={index} />;
      });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-stone-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-slate-800 rounded-lg">
              <Scale className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900" style={{fontFamily: 'Inter, sans-serif'}}>Nepal Law Assistant</h1>
              <p className="text-slate-600 text-sm">Get guidance on Nepal laws and regulations</p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Input Section */}
          <div className="lg:col-span-2 space-y-6">
            {/* Query Input */}
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-slate-800">
                  <FileText className="h-5 w-5" />
                  Describe Your Legal Problem
                </CardTitle>
                <CardDescription>
                  Explain your legal situation or question related to Nepal law
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  data-testid="legal-query-input"
                  placeholder="Example: I have a property dispute with my neighbor about boundary lines. What are my rights under Nepal law?"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="min-h-[120px] resize-none border-slate-200 focus:border-slate-400 focus:ring-slate-400"
                  style={{fontFamily: 'Inter, sans-serif'}}
                />
                <Button 
                  data-testid="analyze-button"
                  onClick={analyzeQuery}
                  disabled={!query.trim() || loading}
                  className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-3"
                  style={{fontFamily: 'Inter, sans-serif'}}
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Scale className="h-4 w-4 mr-2" />
                      Get Legal Guidance
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Analysis Results */}
            {analysis && (
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <BookOpen className="h-5 w-5" />
                    Legal Analysis
                  </CardTitle>
                  <CardDescription className="flex items-center gap-2 text-slate-500">
                    <Clock className="h-4 w-4" />
                    {formatDateTime(analysis.response.timestamp)}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-slate max-w-none">
                    <div className="bg-slate-50 p-4 rounded-lg mb-4">
                      <h4 className="font-semibold text-slate-700 mb-2">Your Question:</h4>
                      <p className="text-slate-600 italic">{analysis.query.query_text}</p>
                    </div>
                    
                    <Separator className="my-4" />
                    
                    <div className="space-y-3">
                      {formatResponse(analysis.response.response_text)}
                    </div>
                    
                    {analysis.response.relevant_laws.length > 0 && (
                      <>
                        <Separator className="my-6" />
                        <div>
                          <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4" />
                            Relevant Laws Referenced
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {analysis.response.relevant_laws.map((law, index) => (
                              <Badge key={index} variant="secondary" className="bg-slate-100 text-slate-700 hover:bg-slate-200">
                                {law}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </>
                    )}
                    
                    <Separator className="my-6" />
                    
                    <div>
                      <h4 className="font-semibold text-slate-800 mb-3">Sources for Verification</h4>
                      <ul className="list-disc list-inside space-y-1 text-slate-600">
                        {analysis.response.sources.map((source, index) => (
                          <li key={index}>{source}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Recent Queries */}
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-slate-800 text-lg">Recent Queries</CardTitle>
                <CardDescription>Your legal consultation history</CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-[400px]">
                  {history.length === 0 ? (
                    <p className="text-slate-500 text-sm text-center py-8">No previous queries yet</p>
                  ) : (
                    <div className="space-y-3">
                      {history.map((item, index) => (
                        <div key={index} className="p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer" onClick={() => setAnalysis(item)}>
                          <p className="text-sm text-slate-700 line-clamp-2 mb-1">
                            {item.query.query_text}
                          </p>
                          <p className="text-xs text-slate-500">
                            {formatDateTime(item.query.timestamp)}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>

            {/* Legal Disclaimer */}
            <Card className="shadow-lg border-0 bg-amber-50/80 backdrop-blur-sm border-amber-200">
              <CardContent className="pt-4">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm text-amber-800 font-medium mb-1">Legal Disclaimer</p>
                    <p className="text-xs text-amber-700 leading-relaxed">
                      This is an AI assistant providing general legal information. For specific legal advice, please consult with a qualified Nepal lawyer or legal professional.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
