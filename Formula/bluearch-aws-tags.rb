class BluearchAwsTags < Formula
  desc "AWS tagging, lifecycle, tag policy, and FinOps CLI"
  homepage "https://github.com/bluearchio/bluearch-aws-tags"
  url "https://github.com/bluearchio/bluearch-aws-tags/releases/download/v0.12.1/tag-manager_macos_arm64"
  version "v0.12.1"
  sha256 "1861a24d5fb01cea10f0fa12cdd89da3efe38e4e0b7400f8b2f315ca73a84a75"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "tag-manager_macos_arm64" => "tag-manager"
  end

  def post_install
    # Clean up curl-installed binary to avoid PATH conflicts
    # The curl installer puts the binary at ~/.local/bin/tag-manager
    curl_binary = Pathname.new(Dir.home) / ".local" / "bin" / "tag-manager"
    if curl_binary.exist?
      begin
        ohai "Removing old curl-installed binary at #{curl_binary}"
        curl_binary.unlink
        ohai "[OK] Old binary removed successfully"
      rescue Errno::EACCES
        opoo "Permission denied: Cannot remove #{curl_binary}"
        opoo "Run manually: rm ~/.local/bin/tag-manager"
      rescue Errno::EBUSY
        opoo "File is in use: #{curl_binary}"
        opoo "Close any running tag-manager processes, then run: rm ~/.local/bin/tag-manager"
      rescue => e
        opoo "Could not remove #{curl_binary}: #{e.message}"
        opoo "Run manually: rm ~/.local/bin/tag-manager"
      end
    end
  end

  def caveats
    <<~EOS
      bluearch-aws-tags has been installed.

      Getting started:
        tag-manager --help
        tag-manager setup validate

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored in: ~/.tag-manager/
    EOS
  end

  test do
    system "#{bin}/tag-manager", "--version"
  end
end
