import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { Button } from './components/ui/button';
import { Textarea } from './components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { Separator } from './components/ui/separator';
import { ScrollArea } from './components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Scale, BookOpen, FileText, AlertTriangle, Clock, Upload, File, CheckCircle, Camera, Zap, Target, TrendingUp } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [query, setQuery] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [documentHistory, setDocumentHistory] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentAnalysis, setDocumentAnalysis] = useState(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('text');
  const [researchQuery, setResearchQuery] = useState('');
  const [researchLoading, setResearchLoading] = useState(false);
  const [researchResult, setResearchResult] = useState(null);
  const [imageAnalysis, setImageAnalysis] = useState(null);
  const [imageLoading, setImageLoading] = useState(false);
  const [problemSolution, setProblemSolution] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const fileInputRef = useRef(null);
  const imageInputRef = useRef(null);
  const responseEndRef = useRef(null);
  
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
    loadDocumentHistory();
  }, []);

  // Auto-scroll to bottom when streaming
  useEffect(() => {
    if (isStreaming && responseEndRef.current) {
      responseEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [analysis, isStreaming]);

  const loadHistory = async () => {
    try {
      // Try to load from backend first
      const response = await axios.get(`${API}/legal-history/${userSession}`);
      const data = Array.isArray(response.data) ? response.data : [];
      
      if (data.length > 0) {
        setHistory(data);
        // Also save to localStorage as backup
        localStorage.setItem(`history-${userSession}`, JSON.stringify(data));
      } else {
        // Fallback to localStorage if backend has no data
        const localData = localStorage.getItem(`history-${userSession}`);
        if (localData) {
          setHistory(JSON.parse(localData));
        }
      }
    } catch (error) {
      console.error('Error loading history:', error);
      // Fallback to localStorage on error
      try {
        const localData = localStorage.getItem(`history-${userSession}`);
        if (localData) {
          setHistory(JSON.parse(localData));
        }
      } catch (e) {
        setHistory([]);
      }
    }
  };

  const loadDocumentHistory = async () => {
    try {
      const response = await axios.get(`${API}/document-history/${userSession}`);
      const data = Array.isArray(response.data) ? response.data : [];
      setDocumentHistory(data);
    } catch (error) {
      console.error('Error loading document history:', error);
      setDocumentHistory([]);
    }
  };

  const analyzeQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setIsStreaming(true);
    const queryText = query;
    setQuery(''); // Clear input immediately
    
    try {
      // Initialize streaming analysis
      const streamingAnalysis = {
        query: {
          query_text: queryText,
          user_session: userSession,
          timestamp: new Date().toISOString()
        },
        response: {
          response_text: '',
          relevant_laws: [],
          sources: [],
          timestamp: new Date().toISOString()
        }
      };
      
      setAnalysis(streamingAnalysis);
      
      // Use EventSource for Server-Sent Events
      const eventSource = new EventSource(
        `${API}/analyze-legal-problem-stream?` + new URLSearchParams({
          query_text: queryText,
          user_session: userSession
        })
      );
      
      // Alternative: Use fetch with streaming
      const response = await fetch(`${API}/analyze-legal-problem-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query_text: queryText,
          user_session: userSession
        })
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.type === 'content') {
                // Append streaming text
                setAnalysis(prev => ({
                  ...prev,
                  response: {
                    ...prev.response,
                    response_text: prev.response.response_text + data.text
                  }
                }));
              } else if (data.type === 'complete') {
                // Add metadata when complete
                setAnalysis(prev => ({
                  ...prev,
                  response: {
                    ...prev.response,
                    relevant_laws: data.relevant_laws || [],
                    sources: data.sources || []
                  }
                }));
                
                // Save to localStorage
                const finalAnalysis = {
                  query: streamingAnalysis.query,
                  response: {
                    ...streamingAnalysis.response,
                    relevant_laws: data.relevant_laws || [],
                    sources: data.sources || []
                  }
                };
                const currentHistory = [...history, finalAnalysis];
                localStorage.setItem(`history-${userSession}`, JSON.stringify(currentHistory));
                
                loadHistory();
              } else if (data.type === 'error') {
                throw new Error(data.message);
              }
            } catch (e) {
              console.error('Error parsing stream:', e);
            }
          }
        }
      }
      
    } catch (error) {
      console.error('Error analyzing legal problem:', error);
      alert('Error analyzing your legal problem. Please try again.');
    } finally {
      setLoading(false);
      setIsStreaming(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Check file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      if (!allowedTypes.includes(file.type)) {
        alert('Please upload only PDF, DOCX, or TXT files.');
        return;
      }
      
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB.');
        return;
      }
      
      setSelectedFile(file);
    }
  };

  const uploadDocument = async () => {
    if (!selectedFile) return;
    
    setUploadLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('user_session', userSession);
      
      const response = await axios.post(`${API}/upload-document`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setDocumentAnalysis(response.data);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      loadDocumentHistory(); // Refresh document history
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error analyzing your document. Please try again.');
    } finally {
      setUploadLoading(false);
    }
  };

  const conductLegalResearch = async () => {
    if (!researchQuery.trim()) return;
    
    setResearchLoading(true);
    try {
      const response = await axios.post(`${API}/legal-research`, {
        query_text: researchQuery,
        user_session: userSession
      });
      
      setResearchResult(response.data);
      setResearchQuery('');
      
      // Save to localStorage immediately
      const currentHistory = [...history, response.data];
      localStorage.setItem(`history-${userSession}`, JSON.stringify(currentHistory));
      
      loadHistory(); // Refresh history from backend
    } catch (error) {
      console.error('Error conducting legal research:', error);
      alert('Error conducting legal research. Please try again.');
    } finally {
      setResearchLoading(false);
    }
  };

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Check file type
      if (!file.type.startsWith('image/')) {
        alert('Please upload only image files (JPG, PNG, BMP, TIFF).');
        return;
      }
      
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('Image size must be less than 10MB.');
        return;
      }
      
      setSelectedFile(file);
    }
  };

  const analyzeImageProblem = async () => {
    if (!selectedFile) return;
    
    setImageLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('user_session', userSession);
      
      const response = await axios.post(`${API}/analyze-image-problem`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setImageAnalysis(response.data);
      setProblemSolution(response.data.solution);
      setSelectedFile(null);
      if (imageInputRef.current) {
        imageInputRef.current.value = '';
      }
      loadDocumentHistory(); // Refresh history
    } catch (error) {
      console.error('Error analyzing image:', error);
      alert('Error analyzing your image. Please try again with a clearer image.');
    } finally {
      setImageLoading(false);
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
    // Enhanced formatting for new structured responses
    return text
      .split('\n')
      .map((line, index) => {
        const trimmedLine = line.trim();
        
        // Section headers with ###
        if (line.startsWith('###')) {
          return (
            <h3 key={index} className="font-bold text-xl mt-6 mb-3 text-slate-900 border-b-2 border-slate-200 pb-2">
              {line.replace(/###/g, '').trim()}
            </h3>
          );
        }
        
        // Section headers with ##
        if (line.startsWith('##')) {
          return (
            <h4 key={index} className="font-semibold text-lg mt-5 mb-2 text-slate-800">
              {line.replace(/##/g, '').trim()}
            </h4>
          );
        }
        
        // Bold text with **
        if (line.includes('**')) {
          const parts = line.split('**');
          return (
            <p key={index} className="mb-2 text-slate-700 leading-relaxed">
              {parts.map((part, i) => 
                i % 2 === 1 ? <strong key={i} className="font-semibold text-slate-900">{part}</strong> : part
              )}
            </p>
          );
        }
        
        // Situation assessment box (special formatting)
        if (trimmedLine.includes('━━━━━━━━━━━━━━━━━━━━━━━━━━━━')) {
          return <div key={index} className="border-t-2 border-slate-300 my-2"></div>;
        }
        
        // Severity indicators with emojis
        if (trimmedLine.includes('Severity:') || trimmedLine.includes('🟢') || trimmedLine.includes('🟡') || trimmedLine.includes('🔴')) {
          return (
            <div key={index} className="bg-slate-50 p-3 rounded-lg mb-2 border-l-4 border-slate-400">
              <p className="text-slate-800 font-medium">{trimmedLine}</p>
            </div>
          );
        }
        
        // Cost, timeline, success indicators
        if (trimmedLine.includes('NPR') || trimmedLine.includes('timeline:') || trimmedLine.includes('probability:')) {
          return (
            <div key={index} className="bg-blue-50 p-2 rounded mb-2">
              <p className="text-blue-900 text-sm font-medium">{trimmedLine}</p>
            </div>
          );
        }
        
        // Next step indicator
        if (trimmedLine.includes('📍 NEXT STEP') || trimmedLine.includes('NEXT STEP:')) {
          return (
            <div key={index} className="bg-green-100 border-l-4 border-green-500 p-4 my-4 rounded-r-lg">
              <p className="text-green-900 font-semibold text-lg">{trimmedLine}</p>
            </div>
          );
        }
        
        // Warning items (❌ or ✗)
        if (trimmedLine.startsWith('❌') || trimmedLine.startsWith('✗')) {
          return (
            <div key={index} className="flex items-start gap-2 mb-2 text-red-700">
              <span className="text-red-500 font-bold">✗</span>
              <p className="flex-1">{trimmedLine.replace(/^[❌✗]\s*/, '')}</p>
            </div>
          );
        }
        
        // Success items (✅ or ✓)
        if (trimmedLine.startsWith('✅') || trimmedLine.startsWith('✓') || trimmedLine.startsWith('□')) {
          return (
            <div key={index} className="flex items-start gap-2 mb-2 text-green-700">
              <span className="text-green-500 font-bold">{trimmedLine.startsWith('□') ? '☐' : '✓'}</span>
              <p className="flex-1">{trimmedLine.replace(/^[✅✓□]\s*/, '')}</p>
            </div>
          );
        }
        
        // Warning items (⚠️)
        if (trimmedLine.startsWith('⚠️')) {
          return (
            <div key={index} className="flex items-start gap-2 mb-2 text-yellow-700">
              <span className="text-yellow-500 font-bold">⚠</span>
              <p className="flex-1">{trimmedLine.replace(/^⚠️\s*/, '')}</p>
            </div>
          );
        }
        
        // Bullet points
        if (trimmedLine.startsWith('-') || trimmedLine.startsWith('•')) {
          return (
            <li key={index} className="ml-6 mb-1 text-slate-700 list-disc">
              {trimmedLine.replace(/^[-•]\s*/, '')}
            </li>
          );
        }
        
        // Option headers with ⭐
        if (trimmedLine.includes('⭐')) {
          return (
            <div key={index} className="bg-amber-50 border-l-4 border-amber-400 p-3 my-3 rounded-r-lg">
              <p className="text-amber-900 font-bold">{trimmedLine}</p>
            </div>
          );
        }
        
        // Regular paragraphs
        if (trimmedLine) {
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
            {/* Input Tabs */}
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-slate-800">
                  <Scale className="h-5 w-5" />
                  Nepal Legal Assistant
                </CardTitle>
                <CardDescription>
                  Get legal guidance by describing your problem or uploading documents
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="text" className="flex items-center gap-1 text-xs">
                      <FileText className="h-3 w-3" />
                      Query
                    </TabsTrigger>
                    {/* <TabsTrigger value="image" className="flex items-center gap-1 text-xs">
                      <Camera className="h-3 w-3" />
                      Photo
                    </TabsTrigger>
                    <TabsTrigger value="document" className="flex items-center gap-1 text-xs">
                      <Upload className="h-3 w-3" />
                      Document
                    </TabsTrigger> */}
                    <TabsTrigger value="research" className="flex items-center gap-1 text-xs">
                      <BookOpen className="h-3 w-3" />
                      Research
                    </TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="text" className="space-y-4 mt-4">
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
                  </TabsContent>
                  
                  <TabsContent value="image" className="space-y-4 mt-4">
                    <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                      <h4 className="font-semibold text-green-800 mb-2 flex items-center gap-2">
                        <Camera className="h-4 w-4" />
                        Smart Photo Analysis
                      </h4>
                      <p className="text-sm text-green-700">
                        Take a photo or upload an image of any legal document, notice, or letter. Our AI will read it and provide complete solutions.
                      </p>
                    </div>
                    <div className="border-2 border-dashed border-green-300 rounded-lg p-6 text-center">
                      <input
                        ref={imageInputRef}
                        type="file"
                        accept="image/*"
                        onChange={handleImageSelect}
                        className="hidden"
                      />
                      {selectedFile ? (
                        <div className="space-y-3">
                          <div className="flex items-center justify-center gap-2 text-green-600">
                            <CheckCircle className="h-5 w-5" />
                            <span className="font-medium">{selectedFile.name}</span>
                          </div>
                          <p className="text-sm text-slate-500">
                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                          <div className="flex gap-2">
                            <Button
                              onClick={() => imageInputRef.current?.click()}
                              variant="outline"
                              className="flex-1"
                            >
                              Choose Different Image
                            </Button>
                            <Button
                              onClick={analyzeImageProblem}
                              disabled={imageLoading}
                              className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                            >
                              {imageLoading ? (
                                <>
                                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                                  Analyzing...
                                </>
                              ) : (
                                <>
                                  <Zap className="h-4 w-4 mr-2" />
                                  Solve Problem
                                </>
                              )}
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-3">
                          <Camera className="h-12 w-12 text-green-400 mx-auto" />
                          <div>
                            <p className="text-slate-600 font-medium">Upload Legal Document Photo</p>
                            <p className="text-sm text-slate-500">Court notices, tax letters, legal papers, contracts</p>
                          </div>
                          <Button
                            onClick={() => imageInputRef.current?.click()}
                            variant="outline"
                            className="border-green-300 hover:border-green-400"
                          >
                            <Camera className="h-4 w-4 mr-2" />
                            Take Photo / Upload Image
                          </Button>
                        </div>
                      )}
                    </div>
                    <div className="text-xs text-slate-500 space-y-1">
                      <p>• Supported formats: JPG, PNG, BMP, TIFF</p>
                      <p>• Our AI reads text from images and provides complete solutions</p>
                      <p>• Works with handwritten and printed documents</p>
                      <p>• Maximum file size: 10MB</p>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="document" className="space-y-4 mt-4">
                    <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center">
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={handleFileSelect}
                        className="hidden"
                      />
                      {selectedFile ? (
                        <div className="space-y-3">
                          <div className="flex items-center justify-center gap-2 text-green-600">
                            <CheckCircle className="h-5 w-5" />
                            <span className="font-medium">{selectedFile.name}</span>
                          </div>
                          <p className="text-sm text-slate-500">
                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                          <div className="flex gap-2">
                            <Button
                              onClick={() => fileInputRef.current?.click()}
                              variant="outline"
                              className="flex-1"
                            >
                              Choose Different File
                            </Button>
                            <Button
                              onClick={uploadDocument}
                              disabled={uploadLoading}
                              className="flex-1 bg-slate-800 hover:bg-slate-700 text-white"
                            >
                              {uploadLoading ? (
                                <>
                                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                                  Analyzing...
                                </>
                              ) : (
                                <>
                                  <Upload className="h-4 w-4 mr-2" />
                                  Analyze Document
                                </>
                              )}
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-3">
                          <File className="h-12 w-12 text-slate-400 mx-auto" />
                          <div>
                            <p className="text-slate-600 font-medium">Upload Legal Document</p>
                            <p className="text-sm text-slate-500">PDF, DOCX, or TXT files up to 10MB</p>
                          </div>
                          <Button
                            onClick={() => fileInputRef.current?.click()}
                            variant="outline"
                            className="border-slate-300 hover:border-slate-400"
                          >
                            <Upload className="h-4 w-4 mr-2" />
                            Choose File
                          </Button>
                        </div>
                      )}
                    </div>
                    <div className="text-xs text-slate-500 space-y-1">
                      <p>• Supported formats: PDF, Word documents (.docx), Text files (.txt)</p>
                      <p>• Our AI will analyze your document and provide relevant Nepal law guidance</p>
                      <p>• Maximum file size: 10MB</p>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="research" className="space-y-4 mt-4">
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                      <h4 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                        <BookOpen className="h-4 w-4" />
                        Comprehensive Legal Research
                      </h4>
                      <p className="text-sm text-blue-700">
                        Get detailed legal analysis with case precedents, specific law references, and step-by-step procedures.
                      </p>
                    </div>
                    <Textarea
                      placeholder="Example: I need comprehensive research on property inheritance laws in Nepal, including Supreme Court precedents and required procedures for property transfer after death."
                      value={researchQuery}
                      onChange={(e) => setResearchQuery(e.target.value)}
                      className="min-h-[120px] resize-none border-slate-200 focus:border-slate-400 focus:ring-slate-400"
                      style={{fontFamily: 'Inter, sans-serif'}}
                    />
                    <Button 
                      onClick={conductLegalResearch}
                      disabled={!researchQuery.trim() || researchLoading}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3"
                      style={{fontFamily: 'Inter, sans-serif'}}
                    >
                      {researchLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                          Researching...
                        </>
                      ) : (
                        <>
                          <BookOpen className="h-4 w-4 mr-2" />
                          Conduct Legal Research
                        </>
                      )}
                    </Button>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            {/* Document Analysis Results */}
            {documentAnalysis && (
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <File className="h-5 w-5" />
                    Document Analysis: {documentAnalysis.filename}
                  </CardTitle>
                  <CardDescription className="flex items-center gap-2 text-slate-500">
                    <Clock className="h-4 w-4" />
                    {formatDateTime(documentAnalysis.timestamp)}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-slate max-w-none">
                    <div className="space-y-3">
                      {formatResponse(documentAnalysis.analysis)}
                    </div>
                    
                    {documentAnalysis.legal_issues.length > 0 && (
                      <>
                        <Separator className="my-6" />
                        <div>
                          <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4" />
                            Legal Issues Identified
                          </h4>
                          <ul className="list-disc list-inside space-y-1 text-slate-700">
                            {documentAnalysis.legal_issues.map((issue, index) => (
                              <li key={index}>{issue}</li>
                            ))}
                          </ul>
                        </div>
                      </>
                    )}
                    
                    {documentAnalysis.recommendations.length > 0 && (
                      <>
                        <Separator className="my-6" />
                        <div>
                          <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                            <BookOpen className="h-4 w-4" />
                            Recommendations
                          </h4>
                          <ul className="list-disc list-inside space-y-1 text-slate-700">
                            {documentAnalysis.recommendations.map((rec, index) => (
                              <li key={index}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      </>
                    )}
                    
                    {documentAnalysis.relevant_laws.length > 0 && (
                      <>
                        <Separator className="my-6" />
                        <div>
                          <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                            <Scale className="h-4 w-4" />
                            Relevant Laws Referenced
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {documentAnalysis.relevant_laws.map((law, index) => (
                              <Badge key={index} variant="secondary" className="bg-slate-100 text-slate-700 hover:bg-slate-200">
                                {law}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Problem Solution Results */}
            {problemSolution && (
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <Target className="h-5 w-5" />
                    Complete Problem Solution
                    <Badge variant={problemSolution.urgency_level === 'critical' ? 'destructive' : 
                                  problemSolution.urgency_level === 'high' ? 'default' : 'secondary'}>
                      {problemSolution.urgency_level.toUpperCase()}
                    </Badge>
                  </CardTitle>
                  <CardDescription className="flex items-center gap-4 text-slate-500">
                    <span className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {formatDateTime(problemSolution.timestamp)}
                    </span>
                    <span className="flex items-center gap-1">
                      <TrendingUp className="h-4 w-4" />
                      {problemSolution.success_probability}% Success Rate
                    </span>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    
                    {/* Immediate Actions */}
                    {problemSolution.immediate_actions.length > 0 && (
                      <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                        <h4 className="font-semibold text-red-800 mb-3 flex items-center gap-2">
                          <AlertTriangle className="h-4 w-4" />
                          Immediate Actions Required
                        </h4>
                        <ul className="space-y-2">
                          {problemSolution.immediate_actions.map((action, index) => (
                            <li key={index} className="flex items-start gap-2 text-red-700">
                              <span className="bg-red-200 text-red-800 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold mt-0.5">
                                {index + 1}
                              </span>
                              <span className="text-sm">{action}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Step-by-Step Solution */}
                    {problemSolution.step_by_step_solution.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                          <FileText className="h-4 w-4" />
                          Step-by-Step Solution
                        </h4>
                        <div className="space-y-3">
                          {problemSolution.step_by_step_solution.map((step, index) => (
                            <div key={index} className="flex gap-3 p-3 bg-slate-50 rounded-lg">
                              <div className="bg-slate-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold flex-shrink-0">
                                {step.step}
                              </div>
                              <div className="flex-1">
                                <p className="text-slate-700 font-medium">{step.description}</p>
                                {step.timeline && (
                                  <p className="text-xs text-slate-500 mt-1">Timeline: {step.timeline}</p>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Required Documents */}
                    {problemSolution.required_documents.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                          <File className="h-4 w-4" />
                          Required Documents
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {problemSolution.required_documents.map((doc, index) => (
                            <div key={index} className="flex items-center gap-2 p-2 bg-blue-50 rounded text-sm text-blue-700">
                              <CheckCircle className="h-4 w-4 text-blue-500" />
                              {doc}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Official Forms */}
                    {problemSolution.official_forms && problemSolution.official_forms.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                          <FileText className="h-4 w-4" />
                          Official Forms & Procedures
                        </h4>
                        <div className="space-y-3">
                          {problemSolution.official_forms.map((form, index) => (
                            <div key={index} className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                              <div className="flex items-start justify-between mb-2">
                                <h5 className="font-medium text-indigo-800">{form.name}</h5>
                                {form.url && (
                                  <a 
                                    href={form.url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-indigo-600 hover:text-indigo-800 text-sm underline"
                                  >
                                    Download Form
                                  </a>
                                )}
                              </div>
                              <p className="text-sm text-indigo-700 mb-2">{form.description}</p>
                              <div className="text-xs text-indigo-600">
                                <p><strong>Office:</strong> {form.office}</p>
                                {form.required_documents && (
                                  <p><strong>Required:</strong> {form.required_documents.join(', ')}</p>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Similar Cases */}
                    {problemSolution.similar_cases.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                          <BookOpen className="h-4 w-4" />
                          How Others Solved Similar Problems
                        </h4>
                        <div className="space-y-3">
                          {problemSolution.similar_cases.map((case_study, index) => (
                            <div key={index} className="p-4 bg-green-50 rounded-lg border border-green-200">
                              <h5 className="font-medium text-green-800 mb-2">{case_study.case_title}</h5>
                              <p className="text-sm text-green-700 mb-2">{case_study.problem_description}</p>
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-xs">
                                <div>
                                  <span className="font-medium">Solution:</span> {case_study.solution_applied}
                                </div>
                                <div>
                                  <span className="font-medium">Timeline:</span> {case_study.timeline}
                                </div>
                                <div>
                                  <span className="font-medium">Cost:</span> {case_study.cost_involved}
                                </div>
                              </div>
                              <p className="text-sm text-green-600 mt-2 font-medium">
                                Outcome: {case_study.outcome}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Warnings */}
                    {problemSolution.warnings.length > 0 && (
                      <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                        <h4 className="font-semibold text-yellow-800 mb-3 flex items-center gap-2">
                          <AlertTriangle className="h-4 w-4" />
                          Important Warnings
                        </h4>
                        <ul className="space-y-1">
                          {problemSolution.warnings.map((warning, index) => (
                            <li key={index} className="text-sm text-yellow-700 flex items-start gap-2">
                              <span className="text-yellow-500 mt-1">⚠️</span>
                              {warning}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* When to Seek Lawyer */}
                    {problemSolution.when_to_seek_lawyer && (
                      <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                        <h4 className="font-semibold text-purple-800 mb-2 flex items-center gap-2">
                          <Scale className="h-4 w-4" />
                          When to Consult a Lawyer
                        </h4>
                        <p className="text-sm text-purple-700">{problemSolution.when_to_seek_lawyer}</p>
                      </div>
                    )}

                  </div>
                </CardContent>
              </Card>
            )}

            {/* Legal Research Results */}
            {researchResult && (
              <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <BookOpen className="h-5 w-5" />
                    Comprehensive Legal Research
                  </CardTitle>
                  <CardDescription className="flex items-center gap-2 text-slate-500">
                    <Clock className="h-4 w-4" />
                    {formatDateTime(researchResult.response.timestamp)}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-slate max-w-none">
                    <div className="bg-blue-50 p-4 rounded-lg mb-4">
                      <h4 className="font-semibold text-blue-700 mb-2">Research Query:</h4>
                      <p className="text-blue-600 italic">{researchResult.query.query_text}</p>
                    </div>
                    
                    <Separator className="my-4" />
                    
                    <div className="space-y-3">
                      {formatResponse(researchResult.response.response_text)}
                    </div>
                    
                    {researchResult.case_precedents && researchResult.case_precedents.length > 0 && (
                      <>
                        <Separator className="my-6" />
                        <div>
                          <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                            <Scale className="h-4 w-4" />
                            Case Precedents
                          </h4>
                          <div className="bg-slate-50 p-4 rounded-lg">
                            <ul className="list-disc list-inside space-y-1 text-slate-700">
                              {researchResult.case_precedents.map((precedent, index) => (
                                <li key={index} className="text-sm">{precedent}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </>
                    )}
                    
                    {researchResult.response.relevant_laws.length > 0 && (
                      <>
                        <Separator className="my-6" />
                        <div>
                          <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4" />
                            Relevant Laws & Regulations
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {researchResult.response.relevant_laws.map((law, index) => (
                              <Badge key={index} variant="secondary" className="bg-blue-100 text-blue-700 hover:bg-blue-200">
                                {law}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </>
                    )}
                    
                    <Separator className="my-6" />
                    
                    <div>
                      <h4 className="font-semibold text-slate-800 mb-3">Research Sources</h4>
                      <ul className="list-disc list-inside space-y-1 text-slate-600">
                        {researchResult.response.sources.map((source, index) => (
                          <li key={index}>{source}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Text Analysis Results */}
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
                    
                    {/* Streaming indicator */}
                    {isStreaming && (
                      <div className="streaming-indicator">
                        <div className="streaming-dots">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                        <span>Analyzing your legal query...</span>
                      </div>
                    )}
                    
                    <div className="space-y-3 streaming-text">
                      {formatResponse(analysis.response.response_text)}
                      {isStreaming && <span className="typing-cursor"></span>}
                      <div ref={responseEndRef} />
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
            {/* History Tabs */}
            <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-slate-800 text-lg">History</CardTitle>
                <CardDescription>Your legal consultation history</CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="queries" className="w-full">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="queries" className="text-xs">
                      Queries & Research
                    </TabsTrigger>
                    <TabsTrigger value="documents" className="text-xs">
                      Documents
                    </TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="queries" className="mt-4">
                    <ScrollArea className="h-[350px]">
                      {history.length === 0 ? (
                        <p className="text-slate-500 text-sm text-center py-8">No previous queries yet</p>
                      ) : (
                        <div className="space-y-3">
                          {history.map((item, index) => (
                            <div key={index} className="p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer" onClick={() => {setAnalysis(item); setDocumentAnalysis(null); setResearchResult(null);}}>
                              <div className="flex items-start gap-2">
                                <FileText className="h-4 w-4 text-slate-400 mt-0.5 flex-shrink-0" />
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm text-slate-700 line-clamp-2 mb-1">
                                    {item.query.query_text}
                                  </p>
                                  <p className="text-xs text-slate-500">
                                    Query • {formatDateTime(item.query.timestamp)}
                                  </p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </ScrollArea>
                  </TabsContent>
                  
                  <TabsContent value="documents" className="mt-4">
                    <ScrollArea className="h-[350px]">
                      {documentHistory.length === 0 ? (
                        <p className="text-slate-500 text-sm text-center py-8">No documents analyzed yet</p>
                      ) : (
                        <div className="space-y-3">
                          {documentHistory.map((item, index) => (
                            <div key={index} className="p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer" onClick={() => {setDocumentAnalysis(item); setAnalysis(null); setResearchResult(null);}}>
                              <div className="flex items-start gap-2">
                                <File className="h-4 w-4 text-slate-400 mt-0.5 flex-shrink-0" />
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm text-slate-700 font-medium truncate mb-1">
                                    {item.filename}
                                  </p>
                                  <p className="text-xs text-slate-500 mb-1">
                                    {item.file_type.toUpperCase()} • {formatDateTime(item.timestamp)}
                                  </p>
                                  {item.legal_issues.length > 0 && (
                                    <p className="text-xs text-slate-600 line-clamp-1">
                                      {item.legal_issues.length} legal issue{item.legal_issues.length !== 1 ? 's' : ''} identified
                                    </p>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </ScrollArea>
                  </TabsContent>
                </Tabs>
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
