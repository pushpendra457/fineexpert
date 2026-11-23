// User Types
export type UserRole = 'user' | 'admin' | 'moderator'

export interface User {
  id: string
  email: string
  name: string
  avatarUrl?: string | null
  role: UserRole
  isActive: boolean
  createdAt: string
  updatedAt: string
}

// Authentication Types
export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  name: string
  email: string
  password: string
  confirmPassword?: string
}

export interface AuthResponse {
  user: User
  token: string
  refreshToken: string
}

export interface RefreshTokenResponse {
  token: string
  refreshToken?: string
}

// Document Types
export type DocumentStatus = 'pending' | 'processing' | 'completed' | 'failed'

export interface Document {
  id: string
  userId: string
  title: string
  fileName: string
  fileSize: number
  fileType: string
  url: string
  status: DocumentStatus
  description?: string | null
  pageCount?: number
  metadata?: Record<string, unknown>
  createdAt: string
  updatedAt: string
}

export interface DocumentFilterParams {
  page?: number
  pageSize?: number
  search?: string
  status?: DocumentStatus
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

// Citation Types
export interface Citation {
  id: string
  documentId: string
  documentTitle: string
  pageNumber?: number
  snippet: string
  confidence?: number
}

// Chat & Conversation Types
export type MessageRole = 'user' | 'assistant' | 'system'

export interface Message {
  id: string
  conversationId: string
  role: MessageRole
  content: string
  citations?: Citation[]
  createdAt: string
}

export interface Conversation {
  id: string
  userId: string
  title: string
  createdAt: string
  updatedAt: string
  messageCount?: number
  lastMessage?: string
}

export interface ChatMessage {
  content: string
  conversationId?: string
}

// Notification Types
export type NotificationType = 'info' | 'success' | 'warning' | 'error'

export interface Notification {
  id: string
  userId: string
  title: string
  message: string
  type: NotificationType
  isRead: boolean
  link?: string | null
  createdAt: string
}

// Common Pagination & API Types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export interface PaginationParams {
  page?: number
  pageSize?: number
  search?: string
}

export interface ApiError {
  message: string
  code?: string
  status?: number
  errors?: Record<string, string[]>
}

export interface ApiResponse<T = unknown> {
  success: boolean
  data: T
  message?: string
}

// Admin Types
export interface AdminStats {
  totalUsers: number
  activeUsers: number
  totalDocuments: number
  totalConversations: number
  storageUsedBytes: number
}

// UI Types
export interface ToastNotification {
  id: string
  title?: string
  message: string
  type: NotificationType
  duration?: number
}

export type ToastNotificationInput = Omit<ToastNotification, 'id'>
