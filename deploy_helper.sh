#!/bin/bash

# Deploy Helper Script
# 6개 Database 설정 및 배포 완전 자동화

set -e

echo ""
echo "=========================================="
echo "  🚀 YouTube Keyword Analyzer Deploy Helper"
echo "=========================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: 환경 확인
check_environment() {
    echo ""
    log_info "Step 1: Checking environment..."
    echo ""

    # Node.js 확인
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_success "Node.js found: $NODE_VERSION"
    else
        log_error "Node.js not found. Please install Node.js 16+"
        exit 1
    fi

    # Python 확인
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        log_success "Python found: $PYTHON_VERSION"
    else
        log_error "Python not found. Please install Python 3.8+"
        exit 1
    fi

    # Git 확인
    if command -v git &> /dev/null; then
        log_success "Git found"
    else
        log_warning "Git not found (optional)"
    fi
}

# Step 2: 의존성 설치
install_dependencies() {
    echo ""
    log_info "Step 2: Installing dependencies..."
    echo ""

    # Node.js 의존성
    if [ -f "package.json" ]; then
        log_info "Installing Node.js packages..."
        npm install
        log_success "Node.js dependencies installed"
    fi

    # Python 의존성
    if [ -f "requirements.txt" ]; then
        log_info "Installing Python packages..."
        pip install -r requirements.txt
        log_success "Python dependencies installed"
    fi
}

# Step 3: 환경 변수 설정
setup_env() {
    echo ""
    log_info "Step 3: Setting up environment variables..."
    echo ""

    if [ -f ".env.local" ]; then
        log_warning ".env.local already exists"
        read -p "Overwrite? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_warning "Skipping .env.local setup"
            return
        fi
    fi

    # .env.local 생성
    cat > .env.local << 'EOF'
# Notion API
NOTION_API_TOKEN=ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ

# Notion Database IDs
# 다음 Database ID들을 설정하세요:
NOTION_DB_KEYWORD_ANALYSIS=YOUR_DATABASE_ID_HERE
NOTION_DB_TREND_DATA=YOUR_DATABASE_ID_HERE
NOTION_DB_RECOMMENDATIONS=YOUR_DATABASE_ID_HERE
NOTION_DB_COMPETITOR=YOUR_DATABASE_ID_HERE
NOTION_DB_INTENT=YOUR_DATABASE_ID_HERE
NOTION_DB_PREDICTION=YOUR_DATABASE_ID_HERE
EOF

    log_success ".env.local created"
    log_warning "Please edit .env.local and add your Notion Database IDs"
}

# Step 4: Database 설정
setup_databases() {
    echo ""
    log_info "Step 4: Setting up Notion Databases..."
    echo ""

    if [ ! -f ".env.local" ]; then
        log_error ".env.local not found"
        return 1
    fi

    python3 setup_notion_db.py --token "ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ" --verify-only
}

# Step 5: Database 초기화
initialize_databases_step() {
    echo ""
    log_info "Step 5: Initializing Databases..."
    echo ""

    if [ -f "init_databases.py" ]; then
        python3 init_databases.py --config .env.local --add-samples
    fi
}

# Step 6: Database 검증
validate_databases_step() {
    echo ""
    log_info "Step 6: Validating Databases..."
    echo ""

    if [ -f "validate_databases.py" ]; then
        python3 validate_databases.py --config .env.local --full
    fi
}

# Step 7: 로컬 테스트
local_test() {
    echo ""
    log_info "Step 7: Ready for local testing"
    echo ""

    log_success "Environment ready!"
    echo ""
    echo "To start development:"
    echo ""
    echo "  Terminal 1 (Backend):"
    echo "  python -m uvicorn backend:app --reload"
    echo ""
    echo "  Terminal 2 (Frontend):"
    echo "  npm run dev"
    echo ""
    echo "  Then open: http://localhost:3000"
}

# Step 8: Vercel 배포
deploy_to_vercel() {
    echo ""
    log_info "Step 8: Deploying to Vercel..."
    echo ""

    if command -v vercel &> /dev/null; then
        read -p "Deploy to Vercel now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            vercel
            log_success "Deployment completed!"
        fi
    else
        log_warning "Vercel CLI not found. Install with: npm i -g vercel"
    fi
}

# 메인 흐름
main() {
    check_environment
    install_dependencies

    read -p "Setup environment variables? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_env
    fi

    read -p "Setup Notion Databases? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_databases
    fi

    read -p "Initialize Databases? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        initialize_databases_step
    fi

    read -p "Validate Databases? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        validate_databases_step
    fi

    read -p "Ready for local testing? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local_test
    fi

    read -p "Deploy to Vercel? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        deploy_to_vercel
    fi

    echo ""
    log_success "All done!"
    echo ""
}

# 실행
main
