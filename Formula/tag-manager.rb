class TagManager < Formula
  desc "AWS Tag Manager CLI - FinOps, compliance, and cost optimization tool"
  homepage "https://bluearch.io"
  url "https://dist.bluearch.io/tag-manager/v0.4.21/tag-manager_macos_arm64"
  version "v0.4.21"
  sha256 "f348174dfea26d6d65f0bf44673b051b86c34e13d08dff453f0089a43f9808a2"
  license :cannot_represent

  depends_on arch: :arm64

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
      Tag Manager CLI has been installed.

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
