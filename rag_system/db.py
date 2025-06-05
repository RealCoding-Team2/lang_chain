import os
import hashlib
from openai import OpenAI
import chromadb
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class ChromaVectorDB:
    """Chroma DB를 사용한 벡터 데이터베이스"""
    
    def __init__(self, collection_name: str = "rag_collection", persist_directory: str = "./chroma_db"):
        """
        초기화
        
        Args:
            collection_name: 컬렉션 이름
            persist_directory: 데이터 저장 디렉토리
        """
        # OpenAI API 키 설정
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 필요합니다.")
        
        self.openai_base_url = os.getenv("OPENAI_BASE_URL")
        if not self.openai_base_url:
            raise ValueError("OPENAI_BASE_URL 환경변수가 필요합니다.")
        
        # OpenAI 클라이언트 초기화
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Chroma DB 클라이언트 초기화
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = collection_name
        
        # 컬렉션 가져오기 또는 생성
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"기존 컬렉션 '{collection_name}' 연결됨")
        except:
            self.collection = self.client.create_collection(name=collection_name)
            print(f"새 컬렉션 '{collection_name}' 생성됨")
    
    def _get_embedding(self, text: str) -> List[float]:
        """OpenAI로 텍스트 임베딩 생성"""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"임베딩 생성 실패: {e}")
            raise
    
    def _generate_content_hash(self, text: str) -> str:
        """텍스트 내용의 해시값 생성"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _check_existing_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """기존 문서와 중복되지 않는 문서들만 필터링"""
        try:
            # 기존 문서들의 메타데이터 조회
            existing_docs = self.collection.get(
                include=['metadatas']
            )
            
            # 기존 URL과 content_hash 세트 생성
            existing_urls = set()
            existing_hashes = set()
            
            for metadata in existing_docs['metadatas']:
                if 'url' in metadata:
                    existing_urls.add(metadata['url'])
                if 'content_hash' in metadata:
                    existing_hashes.add(metadata['content_hash'])
            
            # 중복되지 않는 문서들만 필터링
            unique_documents = []
            for doc in documents:
                url = doc.get('metadata', {}).get('url', '')
                content_hash = self._generate_content_hash(doc['text'])
                
                # URL 또는 content_hash가 이미 존재하는지 확인
                if url and url in existing_urls:
                    print(f"중복 URL 건너뜀: {url}")
                    continue
                
                if content_hash in existing_hashes:
                    print(f"중복 내용 건너뜀: {doc.get('metadata', {}).get('title', 'Unknown')}")
                    continue
                
                # content_hash를 메타데이터에 추가
                if 'metadata' not in doc:
                    doc['metadata'] = {}
                doc['metadata']['content_hash'] = content_hash
                
                unique_documents.append(doc)
            
            print(f"전체 {len(documents)}개 중 {len(unique_documents)}개가 새로운 문서입니다.")
            return unique_documents
            
        except Exception as e:
            print(f"중복 체크 실패: {e}")
            return documents  # 에러 시 모든 문서 반환
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """
        문서들을 벡터 DB에 추가 (중복 제거)
        
        Args:
            documents: [{"id": str, "text": str, "metadata": dict}] 형태의 문서 리스트
            
        Returns:
            성공 여부
        """
        try:
            # 중복되지 않는 문서들만 필터링
            unique_documents = self._check_existing_documents(documents)
            
            if not unique_documents:
                print("추가할 새로운 문서가 없습니다.")
                return True
            
            ids = []
            texts = []
            embeddings = []
            metadatas = []
            
            for doc in unique_documents:
                # 임베딩 생성
                embedding = self._get_embedding(doc['text'])
                
                ids.append(doc['id'])
                texts.append(doc['text'])
                embeddings.append(embedding)
                metadatas.append(doc.get('metadata', {}))
            
            # Chroma DB에 추가
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            print(f"{len(unique_documents)}개 문서 추가 완료")
            return True
            
        except Exception as e:
            print(f"문서 추가 실패: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5, where: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        쿼리로 유사 문서 검색
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 결과 수
            where: 메타데이터 필터 조건
            
        Returns:
            검색 결과 리스트
        """
        try:
            # 쿼리 임베딩 생성
            query_embedding = self._get_embedding(query)
            
            # 검색 실행
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=['documents', 'metadatas', 'distances']
            )
            
            # 결과 정리
            search_results = []
            for i in range(len(results['ids'][0])):
                search_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'score': 1 - results['distances'][0][i]  # 거리를 유사도로 변환
                })
            
            return search_results
            
        except Exception as e:
            print(f"검색 실패: {e}")
            return []
    
    def delete_documents(self, ids: List[str]) -> bool:
        """
        문서 삭제
        
        Args:
            ids: 삭제할 문서 ID 리스트
            
        Returns:
            성공 여부
        """
        try:
            self.collection.delete(ids=ids)
            print(f"{len(ids)}개 문서 삭제 완료")
            return True
        except Exception as e:
            print(f"문서 삭제 실패: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        컬렉션 통계 정보 조회
        
        Returns:
            통계 정보
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "total_vectors": count
            }
        except Exception as e:
            print(f"통계 조회 실패: {e}")
            return {}
    
    def search_by_metadata(self, query: str, metadata_filter: Dict, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        메타데이터 필터를 적용한 검색
        
        Args:
            query: 검색 쿼리
            metadata_filter: 메타데이터 필터 (예: {"category": "news"})
            top_k: 반환할 결과 수
            
        Returns:
            필터링된 검색 결과
        """
        return self.search(query, top_k, where=metadata_filter) 