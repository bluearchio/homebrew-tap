class BluearchAwsOps < Formula
  desc "AWS operations CLI for recommendations, alerting, and remediation"
  homepage "https://github.com/bluearchio/bluearch-aws-ops"
  url "https://github.com/bluearchio/bluearch-aws-ops/releases/download/v0.13.2/bluearch_macos_arm64"
  version "v0.13.2"
  sha256 "314ec33787446027eac4d3ec54ab74973cf929c17d79c209993763a9506632c3"
  license :cannot_represent

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch_macos_arm64" => "bluearch"
  end

  def post_install
    # Clean up curl-installed binary to avoid PATH conflicts
    curl_binary = Pathname.new(Dir.home) / ".local" / "bin" / "bluearch"
    if curl_binary.exist?
      begin
        ohai "Removing old curl-installed binary at #{curl_binary}"
        curl_binary.unlink
        ohai "[OK] Old binary removed successfully"
      rescue Errno::EACCES
        opoo "Permission denied: Cannot remove #{curl_binary}"
        opoo "Run manually: rm ~/.local/bin/bluearch"
      rescue Errno::EBUSY
        opoo "File is in use: #{curl_binary}"
        opoo "Close any running bluearch processes, then run: rm ~/.local/bin/bluearch"
      rescue => e
        opoo "Could not remove #{curl_binary}: #{e.message}"
        opoo "Run manually: rm ~/.local/bin/bluearch"
      end
    end
  end

  def caveats
    <<~EOS
      bluearch-aws-ops has been installed.

      Getting started:
        bluearch --help
        bluearch scan

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored in: ~/.bluearch/
    EOS
  end

  test do
    system "#{bin}/bluearch", "--version"
  end
end
