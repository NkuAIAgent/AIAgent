from processor import WeChatArticleProcessor

def main():
    """主函数"""
    processor = WeChatArticleProcessor()
    processor.process_all()

if __name__ == "__main__":
    main()
